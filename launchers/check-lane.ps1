# check-lane.ps1 (canon method v1; the acceptance rule, decisions/01).
# The desk runs this before writing any RUNNING or DONE line for a lane.
# It prints facts, not judgement: scheduled task state, live process, receipt, worktree.
#
#   pwsh -NoProfile -File launchers/check-lane.ps1 -Receipt <path to the lane's OUTPUT.md or verdict file> `
#       -Repo <path to the repository> -Worktree <path to the lane's worktree> `
#       -Branch <the lane's branch> [-SourceFile package.json] [-Task <scheduled task name>] [-ProcessName codex]
#
# Every path is an argument; nothing is assumed about where the operator keeps things.
param(
  [string]$Task,
  [string]$Receipt,
  [string]$Repo,
  [string]$Worktree,
  [string]$Branch,
  [string]$SourceFile = 'package.json',
  [string]$ProcessName = 'codex'
)
$lines = @()
if ($Task) {
  $t = Get-ScheduledTask -TaskName $Task -ErrorAction SilentlyContinue
  if ($t) { $lines += "TASK $Task : $($t.State)" } else { $lines += "TASK $Task : NOT REGISTERED" }
}
if ($ProcessName) {
  $recent = Get-Process $ProcessName -ErrorAction SilentlyContinue | Where-Object { $_.StartTime -gt (Get-Date).AddHours(-6) }
  $lines += "PROCESS ${ProcessName}: $(@($recent).Count) started in the last 6 hours"
}
if ($Receipt) {
  if (Test-Path -LiteralPath $Receipt) {
    $f = Get-Item -LiteralPath $Receipt
    $last = (Get-Content -LiteralPath $Receipt | Where-Object { $_ -match '^STATUS:' } | Select-Object -Last 1)
    $age = [int]((Get-Date) - $f.LastWriteTime).TotalMinutes
    $lines += "RECEIPT present: $($f.Length) bytes, last written $age min ago, created $($f.CreationTime.ToString('HH:mm'))"
    $lines += "RECEIPT last status: $last"
    $pre = Get-Content -LiteralPath $Receipt | Select-String -Pattern 'Preflight|branch|HEAD|cwd' | Select-Object -First 2
    foreach ($p in $pre) { $lines += "RECEIPT preflight: $($p.Line.Substring(0, [Math]::Min(160, $p.Line.Length)))" }
  } else { $lines += "RECEIPT MISSING: $Receipt" }
}
if ($Repo -and $Worktree) {
  if (Test-Path -LiteralPath $Worktree) { $Worktree = (Resolve-Path -LiteralPath $Worktree).Path }
  $wt = (& git -C $Repo worktree list) -join "`n"
  $norm = $Worktree.Replace('\','/')
  if ($wt -match [regex]::Escape($norm)) { $lines += "WORKTREE registered at the intended path: YES" } else { $lines += "WORKTREE registered at the intended path: NO (git worktree list does not show $norm)" }
  if (Test-Path -LiteralPath (Join-Path $Worktree $SourceFile)) { $lines += "WORKTREE source file ${SourceFile}: PRESENT" } else { $lines += "WORKTREE source file ${SourceFile}: MISSING" }
  if ($Branch) {
    $cur = & git -C $Worktree branch --show-current 2>$null
    if ($cur -eq $Branch) { $lines += "WORKTREE branch: $cur (matches)" } else { $lines += "WORKTREE branch: '$cur' (expected $Branch)" }
  }
}
$lines | ForEach-Object { Write-Output $_ }
