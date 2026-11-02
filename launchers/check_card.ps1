<#
check_card.ps1 (canon method v1): the card gate the desk runs before firing a Claude lane with the Agent tool
(skills/fire-opus-worker). It is the same checker launchers/fire-codex-job.ps1 runs for a Codex card.

  pwsh -NoProfile -File launchers/check_card.ps1 -Card <CARD.md path> [-Form auto|claude|codex] [-WithholdWords]

Runs tools/card_check.py on one card and prints its lines.
Exit 0 only on PASS; any FAIL, a missing checker, an unreadable card, or a card that changed during the check exits 1.
-Form auto (the default) reads a card starting "# CARD:" as the Claude lane form, anything else as the Codex form.
Python 3 must be on the path.
#>
param(
  [Parameter(Mandatory = $true)] [string] $Card,
  [ValidateSet('auto', 'claude', 'codex')] [string] $Form = 'auto',
  [switch] $WithholdWords
)
$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSVersion.Major -lt 7) { Write-Host 'pwsh 7 required'; exit 1 }
$status = 'failed'
$output = @()
try {
  if (-not (Test-Path -LiteralPath $Card -PathType Leaf)) { throw "card not found: $Card" }
  $checker = Join-Path (Split-Path -Parent $PSScriptRoot) 'tools\card_check.py'
  if (-not (Test-Path -LiteralPath $checker -PathType Leaf)) { throw "Card checker missing: $checker" }
  $python = (Get-Command python -ErrorAction SilentlyContinue).Source
  if (-not $python) { throw 'python not found on the path' }
  $cardText = Get-Content -LiteralPath $Card -Raw
  $checkArgs = @($checker, $Card, '--form', $Form)
  if ($WithholdWords) { $checkArgs += '--withhold-words' }
  $output = @(& $python @checkArgs 2>&1 | ForEach-Object { "$_" })
  $passed = ($LASTEXITCODE -eq 0) -and ($output -contains 'PASS')
  if ($passed -and (Get-Content -LiteralPath $Card -Raw) -cne $cardText) {
    $passed = $false
    $output += 'Card changed during the card check.'
  }
  $status = if ($passed) { 'passed' } else { 'failed' }
} catch {
  $status = 'failed'
  $output += $_.Exception.Message
}
$output | ForEach-Object { Write-Host $_ }
Write-Host "card check result: $status"
if ($status -ne 'passed') {
  Write-Host 'Card check failed. Fix the card and rerun before any Agent call.'
  exit 1
}
exit 0
