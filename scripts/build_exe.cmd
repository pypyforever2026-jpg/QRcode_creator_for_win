@echo off
setlocal

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Create it with: py -3 -m venv .venv
    exit /b 1
)

".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 exit /b 1

".venv\Scripts\python.exe" -m pip install -r requirements.txt -r requirements-build.txt
if errorlevel 1 exit /b 1

".venv\Scripts\python.exe" -m pip install -e .
if errorlevel 1 exit /b 1

".venv\Scripts\python.exe" -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --onefile ^
    --windowed ^
    --name ProductQRCodeMaker ^
    --paths src ^
    src\qrcode_product_maker\__main__.py
if errorlevel 1 exit /b 1

echo Done: dist\ProductQRCodeMaker.exe

