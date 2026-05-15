$ErrorActionPreference = "Stop"

function Get-PythonCommand {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return "py"
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return "python"
    }
    throw "Python is not installed or not in PATH. Install Python 3.10+ and retry."
}

$pythonCmd = Get-PythonCommand

if (-not (Test-Path ".venv")) {
    if ($pythonCmd -eq "py") {
        py -m venv .venv
    } else {
        python -m venv .venv
    }
}

. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

if ((Get-Item "requirements.txt").Length -gt 0) {
    python -m pip install -r requirements.txt
}

Write-Host "Install complete."
Write-Host "Run demo: .\.venv\Scripts\python.exe src/app.py --reset-memory"
Write-Host "Run website: .\.venv\Scripts\python.exe -m http.server 5500"
