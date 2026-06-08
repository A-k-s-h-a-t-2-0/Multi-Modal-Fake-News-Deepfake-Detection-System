$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $ProjectRoot

& ".\.venv\Scripts\python.exe" -m streamlit run app.py `
  --server.port 8501 `
  --server.headless true `
  --server.fileWatcherType none
