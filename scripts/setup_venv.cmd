@echo off
py -3 -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
echo.
echo Ready. Run the app with:
echo python -m qrcode_product_maker
