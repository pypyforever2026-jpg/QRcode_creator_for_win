"""Tests for QR payload generation."""

from qrcode_product_maker.models import ProductQRData


def test_payload_contains_required_product_name() -> None:
    """Product name should always be present in the payload."""
    payload = ProductQRData(product_name="Green Tea").to_payload()

    assert payload == "Product Name: Green Tea"


def test_payload_includes_only_filled_optional_fields() -> None:
    """Optional fields should appear only when they contain text."""
    payload = ProductQRData(
        product_name="Milk",
        production_date="2026-05-10",
        expiration_date="",
        description="Keep refrigerated.",
    ).to_payload()

    assert "Product Name: Milk" in payload
    assert "Production Date: 2026-05-10" in payload
    assert "Expiration Date:" not in payload
    assert "Description: Keep refrigerated." in payload
