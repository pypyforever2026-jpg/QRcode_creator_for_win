# Product QR Code Maker

Product QR Code Maker is a clean Windows desktop application for creating
print-ready QR codes for product labels, packaging, inventory tags, and small
batch workflows.

The interface is fully English. The QR payload is UTF-8 text, so users can still
enter international product names and descriptions when needed.

## Highlights

- Required product name field.
- Optional production date, expiration date, and description fields.
- Built-in Gregorian date picker for production and expiration dates.
- Optional fields are included in the QR code only when they contain text.
- Print-focused QR sizing in millimeters.
- Selectable DPI for label and packaging output.
- Save as PNG, JPEG, BMP, TIFF, or WebP.
- Send the generated QR code directly to the Windows print flow.
- Modular Python code with English docstrings.
- One-file Windows executable build script.

## Screens

The app opens directly to the QR creation form:

- Product details on the left.
- Live QR preview and encoded text preview on the right.
- Save and Print actions below the preview.

## Requirements

For Windows 10 and Windows 11, Python 3.10 or newer is suitable for development.

For Windows 7 compatibility, use Python 3.8.10. Build a 32-bit executable with
32-bit Python, and a 64-bit executable with 64-bit Python.

## Setup

Create the virtual environment with:

```cmd
py -3 -m venv .venv
```

Activate it:

```cmd
.venv\Scripts\activate
```

Install the project:

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

Run the app:

```cmd
python -m qrcode_product_maker
```

## Build The EXE

From Command Prompt:

```cmd
scripts\build_exe.cmd
```

Or from PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_exe.ps1
```

The standalone executable is created at:

```text
dist\ProductQRCodeMaker.exe
```

End users do not need Python or any project dependencies installed.

## GitHub Builds

This repository includes a GitHub Actions workflow that can build both 32-bit
and 64-bit Windows executables. Push the project to GitHub and run the
`Build Windows EXE` workflow from the Actions tab.

## Project Layout

```text
src/qrcode_product_maker/
  __main__.py       Application entry point
  app.py            Tkinter desktop interface
  date_picker.py    Gregorian date picker widget
  models.py         Product QR payload model
  qr_service.py     QR rendering and image export logic
  printing.py       Windows printing helper
  validators.py     Input validation helpers
scripts/
  build_exe.cmd     Builds a standalone executable from Command Prompt
  build_exe.ps1     Builds a standalone executable from PowerShell
  setup_venv.cmd    Creates the virtual environment and installs the app
```

## License

MIT
