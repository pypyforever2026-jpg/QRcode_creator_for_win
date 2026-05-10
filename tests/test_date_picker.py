"""Tests for Gregorian date helpers."""

from qrcode_product_maker.date_picker import SelectedDate


def test_selected_date_display_value() -> None:
    """Selected dates should use an ISO-style date format."""
    selected = SelectedDate(year=2026, month=5, day=10)

    assert selected.display_value() == "2026-05-10"
