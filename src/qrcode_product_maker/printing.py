"""Windows printing helpers."""

import os
import tempfile
from pathlib import Path

from PIL import Image

from qrcode_product_maker.qr_service import DEFAULT_DPI, save_image


def print_image_with_windows(image: Image.Image, dpi: int = DEFAULT_DPI) -> Path:
    """Send an image to the Windows print action and return the temporary file path."""
    temp_dir = Path(tempfile.gettempdir())
    temp_path = temp_dir / "product_qr_code_to_print.png"
    save_image(image, str(temp_path), dpi=dpi)
    os.startfile(str(temp_path), "print")
    return temp_path

