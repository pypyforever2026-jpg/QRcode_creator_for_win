"""Validation helpers for user input."""


def validate_product_name(value: str) -> str:
    """Return a cleaned product name or raise ValueError when it is empty."""
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Product name is required.")
    return cleaned


def validate_positive_float(value: str, field_name: str) -> float:
    """Return a positive float parsed from user input."""
    try:
        number = float(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a number.") from exc

    if number <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")
    return number


def validate_positive_int(value: str, field_name: str) -> int:
    """Return a positive integer parsed from user input."""
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a whole number.") from exc

    if number <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")
    return number
