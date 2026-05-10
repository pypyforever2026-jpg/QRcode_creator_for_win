$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Virtual environment not found. Create it with: py -3 -m venv .venv"
    exit 1
}

& ".venv\Scripts\python.exe" -m pip install --upgrade pip
& ".venv\Scripts\python.exe" -m pip install -r requirements.txt -r requirements-build.txt
& ".venv\Scripts\python.exe" -m pip install -e .

& ".venv\Scripts\python.exe" -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name ProductQRCodeMaker `
    --paths src `
    src\qrcode_product_maker\__main__.py

Write-Host "Done: dist\ProductQRCodeMaker.exe"
