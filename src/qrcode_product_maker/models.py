"""Data models for product QR code generation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProductQRData:
    """Product information that will be encoded into a QR code."""

    product_name: str
    production_date: str = ""
    expiration_date: str = ""
    description: str = ""

    def to_payload(self) -> str:
        """Return a UTF-8 friendly text payload with labels for filled fields."""
        lines = [f"Product Name: {self.product_name.strip()}"]

        optional_fields = (
            ("Production Date", self.production_date),
            ("Expiration Date", self.expiration_date),
            ("Description", self.description),
        )
        for label, value in optional_fields:
            clean_value = value.strip()
            if clean_value:
                lines.append(f"{label}: {clean_value}")

        return "\n".join(lines)
