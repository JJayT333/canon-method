<#
fire-codex-job.ps1 (canon method v1): run one card as a headless Codex job from the desk.

  pwsh -NoProfile -File launchers/fire-codex-job.ps1 -Card <CARD.md> -Cwd <folder the job works in>
       [-Model <model>] [-Name <short>] [-Config <config.json>] [-Memories] [-SkipCardCheck] [-DryRun]

The job reads its card, works in -Cwd (the product worktree for a fix, the record folder for a check),
and writes its record next to the card: evidence/CODEX.log (transcript), CODEX-LAST.md (last message),
CODEX-RUN.md (the receipt: card check, engine, model, timing, exit code), evidence/PROMPT.txt (what was sent).

Paths come from the config file: ../config.json beside this folder, else ../config.example.json, else -Config.
  codex_exe        full path to codex.exe; when empty the newest engine under codex_bin_dir is used
  codex_bin_dir    the Codex app's engine folder (default %LOCALAPPDATA%\OpenAI\Codex\bin); env vars expand
  default_codex_model   used when -Model is not given; empty means the engine's own default
  worker_name      what the prompt calls the worker
  protected_paths  folders the worker is told never to touch (the operator's live checkout)
  protected_ports  ports the worker is told never to use

The card checker (../tools/card_check.py) refuses failing cards before engine discovery unless -SkipCardCheck.
-DryRun checks the card, writes the receipt and exits without starting Codex. Memories are off unless -Memories.
A checker card must never pass -Memories. The job runs on the Codex app's own login; every ANTHROPIC_* and OPENAI_* environment variable is cleared first.
#>
param(
  [Parameter(Mandatory = $true)] [string] $Card,
  [Parameter(Mandatory = $true)] [string] $Cwd,
  [string] $Model = '',
  [string] $Name = '',
  [string] $Config = '',
  [switch] $Memories,
  [switch] $SkipCardCheck,
  [switch] $DryRun
)
$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSVersion.Major -lt 7) { throw 'pwsh 7 required' }
if (-not (Test-Path -LiteralPath $Card)) { throw "card not found: $Card" }
if (-not (Test-Path -LiteralPath $Cwd)) { throw "working folder not found: $Cwd" }

$root = Split-Path -Parent $PSScriptRoot
if ($Config -eq '') {
  $Config = Join-Path $root 'config.json'
  if (-not (Test-Path -LiteralPath $Config)) { $Config = Join-Path $root 'config.example.json' }
}
if (-not (Test-Path -LiteralPath $Config)) { throw "config not found: $Config" }
$cfg = Get-Content -LiteralPath $Config -Raw | ConvertFrom-Json
function Get-Cfg([string] $name, $default) {
  $p = $cfg.PSObject.Properties[$name]
  if ($p -and $null -ne $p.Value -and "$($p.Value)" -ne '') { return $p.Value } else { return $default }
}
$workerName = Get-Cfg 'worker_name' 'the Codex worker'
$protectedPaths = @(Get-Cfg 'protected_paths' @())
$protectedPorts = @(Get-Cfg 'protected_ports' @())
if ($Model -eq '') { $Model = Get-Cfg 'default_codex_model' '' }

$Card = (Resolve-Path -LiteralPath $Card).Path
$Cwd = (Resolve-Path -LiteralPath $Cwd).Path
$cardDir = Split-Path -Parent $Card
if ($Name -eq '') { $Name = Split-Path -Leaf $cardDir }
$evidence = Join-Path $cardDir 'evidence'
New-Item -ItemType Directory -Force -Path $evidence | Out-Null
$log = Join-Path $evidence 'CODEX.log'
$last = Join-Path $cardDir 'CODEX-LAST.md'
$run = Join-Path $cardDir 'CODEX-RUN.md'
$start = Get-Date
$checkStatus = if ($SkipCardCheck) { 'skipped' } else { 'checking' }
"# Codex job $Name`n- card: $Card`n- cwd: $Cwd`n- config: $Config`n- card check: $checkStatus`n- started: $($start.ToString('yyyy-MM-dd HH:mm'))" | Set-Content -LiteralPath $run
$cardText = Get-Content -LiteralPath $Card -Raw

if (-not $SkipCardCheck) {
  $checkOutput = @()
  try {
    $checker = Join-Path $root 'tools\card_check.py'
    if (-not (Test-Path -LiteralPath $checker -PathType Leaf)) { throw "Card checker missing: $checker" }
    $checkOutput = @(& python $checker $Card 2>&1 | ForEach-Object { "$_" })
    $checkStatus = if ($LASTEXITCODE -eq 0) { 'passed' } else { 'failed' }
    if ($checkStatus -eq 'passed' -and (Get-Content -LiteralPath $Card -Raw) -cne $cardText) {
      $checkStatus = 'failed'
      $checkOutput += 'Card changed during the card check. No Codex started.'
    }
  } catch {
    $checkStatus = 'failed'
    $checkOutput += $_.Exception.Message
  }
  $checkOutput | ForEach-Object { Write-Host $_; "  $_" | Add-Content -LiteralPath $run }
  "- card check result: $checkStatus" | Add-Content -LiteralPath $run
  if ($checkStatus -ne 'passed') {
    '- execution: failed (card check; no Codex started)' | Add-Content -LiteralPath $run
    Write-Error 'Card check failed. No Codex started.' -ErrorAction Continue
    exit 1
  }
} else {
  '- card check result: skipped (override)' | Add-Content -LiteralPath $run
}

$never = @()
if ($protectedPaths.Count -gt 0) { $never += "Never touch these folders: $($protectedPaths -join ', ')." }
if ($protectedPorts.Count -gt 0) { $never += "Never use these ports: $($protectedPorts -join ', ')." }
$prompt = "You are $workerName, running headless from the desk. Your card is the file $Card. Read it whole and do it. Your record folder is $cardDir (write OUTPUT.md there in your first minute with STATUS: RUNNING as its last line, append each part the moment it is done, STATUS last). You are working in $Cwd. $($never -join ' ') Never merge, never push to main, never add a remote. No em-dashes."
$promptFile = Join-Path $evidence 'PROMPT.txt'
Set-Content -LiteralPath $promptFile -Value $prompt -NoNewline -Encoding utf8

if ($DryRun) {
  "- model: $(if ($Model) { $Model } else { 'engine default' })`n- execution: dry run (card checked, prompt written to evidence/PROMPT.txt, no Codex started)" | Add-Content -LiteralPath $run
  Write-Host "Dry run: card passed, receipt at $run"
  exit 0
}

$engine = Get-Cfg 'codex_exe' ''
if ($engine -eq '') {
  $binDir = [Environment]::ExpandEnvironmentVariables((Get-Cfg 'codex_bin_dir' '%LOCALAPPDATA%\OpenAI\Codex\bin'))
  if (-not (Test-Path -LiteralPath $binDir)) { throw "Codex engine folder not found: $binDir (set codex_exe or codex_bin_dir in $Config)" }
  $engine = Get-ChildItem -LiteralPath $binDir -Directory | ForEach-Object { Join-Path $_.FullName 'codex.exe' } | Where-Object { Test-Path -LiteralPath $_ } | Sort-Object { (Get-Item -LiteralPath $_).LastWriteTime } -Descending | Select-Object -First 1
  if (-not $engine) { $engine = Join-Path $binDir 'codex.exe' }
}
if (-not (Test-Path -LiteralPath $engine)) { throw "no Codex engine found at $engine" }
Get-ChildItem Env: | Where-Object { $_.Name -match '^(ANTHROPIC|OPENAI)_' } | ForEach-Object { Remove-Item -LiteralPath "Env:$($_.Name)" -ErrorAction SilentlyContinue }

"- engine: $engine ($((& $engine --version 2>&1 | Select-Object -First 1)))`n- model: $(if ($Model) { $Model } else { 'engine default' })`n- memories: $($Memories.IsPresent.ToString().ToLowerInvariant()) (per-run features.memories override)`n- stdin: prompt from evidence/PROMPT.txt, then closed" | Add-Content -LiteralPath $run

$engineArgs = @('exec', '--cd', $Cwd, '--skip-git-repo-check', '--output-last-message', $last, '-c', "features.memories=$($Memories.IsPresent.ToString().ToLowerInvariant())")
if ($Model -ne '') { $engineArgs += @('--model', $Model) }
$engineArgs += '-'
$actualModelHeader = $null
Get-Content -LiteralPath $promptFile -Raw | & $engine @engineArgs 2>&1 | ForEach-Object {
  $line = "$_"
  if (-not $actualModelHeader -and $line -match '^model:\s+\S+') {
    $actualModelHeader = $line
    "- actual engine model header: $actualModelHeader" | Add-Content -Path $run
  }
  $line
} | Tee-Object -FilePath $log | Out-Null
$code = $LASTEXITCODE
if (-not $actualModelHeader) { '- actual engine model header: unavailable (engine did not emit one)' | Add-Content -Path $run }
$end = Get-Date
"- ended: $($end.ToString('yyyy-MM-dd HH:mm'))`n- minutes: $([math]::Round(($end - $start).TotalMinutes, 1))`n- exit code: $code" | Add-Content -Path $run
exit $code
