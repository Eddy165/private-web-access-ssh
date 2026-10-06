$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
Write-Host "Starting private web service on 127.0.0.1:8000..."
python .\private_web\server.py
