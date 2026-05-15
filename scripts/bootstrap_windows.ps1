$ErrorActionPreference = "Stop"

$repoUrl = "https://github.com/Ranojitdas/Finance-app-jac.git"
$targetDir = "Finance-app-jac"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git is required but not found. Install git and retry."
}

if (-not (Test-Path $targetDir)) {
    git clone $repoUrl $targetDir
}

Set-Location $targetDir
powershell -ExecutionPolicy Bypass -File scripts/install_windows.ps1

Write-Host ""
Write-Host "Next:"
Write-Host "cd $targetDir"
Write-Host ".\.venv\Scripts\python.exe src/app.py --reset-memory"
