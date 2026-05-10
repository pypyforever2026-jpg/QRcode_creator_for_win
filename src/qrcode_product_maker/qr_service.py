"""QR code rendering and image saving services."""

from pathlib import Path
from typing import Tuple

import qrcode
from PIL import Image

MM_PER_INCH = 25.4
DEFAULT_DPI = 300


def millimeters_to_pixels(size_mm: float, dpi: int = DEFAULT_DPI) -> int:
    """Convert a physical size in millimeters to pixels for the selected DPI."""
    return max(1, round((size_mm / MM_PER_INCH) * dpi))


def create_qr_image(payload: str, size_mm: float, dpi: int = DEFAULT_DPI) -> Image.Image:
    """Create a square QR code image sized for print output."""
    target_pixels = millimeters_to_pixels(size_mm, dpi)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    resampling_filter = getattr(Image, "Resampling", Image).NEAREST
    return image.resize((target_pixels, target_pixels), resampling_filter)


def save_image(image: Image.Image, path: str, dpi: int = DEFAULT_DPI) -> None:
    """Save a QR code image using a format inferred from the file extension."""
    output_path = Path(path)
    extension = output_path.suffix.lower()

    if extension in {".jpg", ".jpeg"}:
        image.save(output_path, "JPEG", quality=95, dpi=(dpi, dpi))
        return

    if extension == ".bmp":
        image.save(output_path, "BMP")
        return

    if extension in {".tif", ".tiff"}:
        image.save(output_path, "TIFF", dpi=(dpi, dpi))
        return

    if extension == ".webp":
        image.save(output_path, "WEBP", quality=95)
        return

    image.save(output_path, "PNG", dpi=(dpi, dpi))


def get_preview_size(image: Image.Image, max_size: int = 260) -> Tuple[int, int]:
    """Return dimensions that fit an image into a square preview area."""
    width, height = image.size
    scale = min(max_size / width, max_size / height, 1)
    return max(1, int(width * scale)), max(1, int(height * scale))

