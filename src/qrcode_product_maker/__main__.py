"""Application entry point."""

from qrcode_product_maker.app import ProductQRCodeApp


def main() -> None:
    """Start the desktop application."""
    app = ProductQRCodeApp()
    app.mainloop()


if __name__ == "__main__":
    main()

