"""Tkinter desktop interface for Product QR Code Maker."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from PIL import Image, ImageTk

from qrcode_product_maker.date_picker import DateInput
from qrcode_product_maker.models import ProductQRData
from qrcode_product_maker.printing import print_image_with_windows
from qrcode_product_maker.qr_service import (
    DEFAULT_DPI,
    create_qr_image,
    get_preview_size,
    save_image,
)
from qrcode_product_maker.validators import (
    validate_positive_float,
    validate_positive_int,
    validate_product_name,
)


class ProductQRCodeApp(tk.Tk):
    """Main desktop window for creating, previewing, saving, and printing QR codes."""

    def __init__(self) -> None:
        """Initialize the application window and widgets."""
        super().__init__()
        self.title("Product QR Code Maker")
        self.geometry("840x600")
        self.minsize(780, 560)

        self.current_image: Optional[Image.Image] = None
        self.preview_image: Optional[ImageTk.PhotoImage] = None

        self.product_name_var = tk.StringVar()
        self.size_mm_var = tk.StringVar(value="30")
        self.dpi_var = tk.StringVar(value=str(DEFAULT_DPI))
        self.status_var = tk.StringVar(
            value="Enter product details, choose print size, and generate a QR code."
        )

        self._configure_style()
        self._build_layout()

    def _configure_style(self) -> None:
        """Configure basic Tkinter theme styling."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(background="#f3f6f8")

        style = ttk.Style(self)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure(".", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Action.TButton", padding=(12, 10), font=("Segoe UI", 10, "bold"))
        style.configure("Status.TLabel", foreground="#334155")

    def _build_layout(self) -> None:
        """Create and arrange all visible widgets."""
        container = ttk.Frame(self, padding=18)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(1, weight=1)

        title = ttk.Label(container, text="Product QR Code Maker", style="Title.TLabel")
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        form = ttk.LabelFrame(container, text="Product details", padding=14)
        form.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        form.columnconfigure(1, weight=1)

        self._add_entry(form, 0, "Product name *", self.product_name_var)
        self.production_date_input = self._add_date_input(form, 1, "Production date")
        self.expiration_date_input = self._add_date_input(form, 2, "Expiration date")

        description_label = ttk.Label(form, text="Description")
        description_label.grid(row=3, column=0, sticky="nw", pady=7)
        self.description_text = tk.Text(form, height=7, wrap="word", font=("Segoe UI", 10))
        self.description_text.configure(
            borderwidth=1,
            relief="solid",
            highlightthickness=0,
            padx=8,
            pady=6,
        )
        self.description_text.grid(row=3, column=1, sticky="ew", pady=7)

        size_label = ttk.Label(form, text="QR size (mm)")
        size_label.grid(row=4, column=0, sticky="w", pady=7)
        size_spin = ttk.Spinbox(form, from_=10, to=200, increment=1, textvariable=self.size_mm_var)
        size_spin.grid(row=4, column=1, sticky="ew", pady=7)

        dpi_label = ttk.Label(form, text="Print DPI")
        dpi_label.grid(row=5, column=0, sticky="w", pady=7)
        dpi_combo = ttk.Combobox(
            form,
            textvariable=self.dpi_var,
            values=("150", "203", "300", "600"),
            state="normal",
        )
        dpi_combo.grid(row=5, column=1, sticky="ew", pady=7)

        generate_button = ttk.Button(
            form,
            text="Generate QR Code",
            style="Action.TButton",
            command=self.generate_qr_code,
        )
        generate_button.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(16, 6))

        output = ttk.LabelFrame(container, text="Preview", padding=14)
        output.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        output.columnconfigure(0, weight=1)
        output.rowconfigure(0, weight=1)

        self.preview_label = ttk.Label(output, anchor="center", text="No QR code generated yet")
        self.preview_label.grid(row=0, column=0, sticky="nsew", pady=(0, 12))

        self.payload_preview = tk.Text(output, height=7, wrap="word", font=("Consolas", 9))
        self.payload_preview.configure(borderwidth=1, relief="solid", padx=8, pady=6)
        self.payload_preview.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        self.payload_preview.configure(state="disabled")

        button_row = ttk.Frame(output)
        button_row.grid(row=2, column=0, sticky="ew")
        button_row.columnconfigure(0, weight=1)
        button_row.columnconfigure(1, weight=1)

        save_button = ttk.Button(button_row, text="Save", command=self.save_current_qr_code)
        save_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        print_button = ttk.Button(button_row, text="Print", command=self.print_current_qr_code)
        print_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        status = ttk.Label(
            container,
            textvariable=self.status_var,
            anchor="w",
            style="Status.TLabel",
        )
        status.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(14, 0))

    def _add_entry(
        self,
        parent: ttk.LabelFrame,
        row: int,
        label_text: str,
        variable: tk.StringVar,
    ) -> None:
        """Add a labeled single-line text input to the form."""
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky="w", pady=7)
        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row, column=1, sticky="ew", pady=7)

    def _add_date_input(self, parent: ttk.LabelFrame, row: int, label_text: str) -> DateInput:
        """Add a labeled date picker input to the form."""
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky="w", pady=7)
        date_input = DateInput(parent, label_text)
        date_input.grid(row=row, column=1, sticky="ew", pady=7)
        return date_input

    def _collect_form_data(self) -> ProductQRData:
        """Read, validate, and return form data."""
        product_name = validate_product_name(self.product_name_var.get())
        return ProductQRData(
            product_name=product_name,
            production_date=self.production_date_input.get(),
            expiration_date=self.expiration_date_input.get(),
            description=self.description_text.get("1.0", "end").strip(),
        )

    def generate_qr_code(self) -> None:
        """Generate a QR code from the current form values."""
        try:
            data = self._collect_form_data()
            size_mm = validate_positive_float(self.size_mm_var.get(), "QR size")
            dpi = validate_positive_int(self.dpi_var.get(), "DPI")
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        payload = data.to_payload()
        self.current_image = create_qr_image(payload, size_mm=size_mm, dpi=dpi)
        self._update_preview(self.current_image, payload)
        self.status_var.set(
            "Generated QR code at "
            f"{self.current_image.size[0]} x {self.current_image.size[1]} "
            "pixels."
        )

    def _update_preview(self, image: Image.Image, payload: str) -> None:
        """Refresh the image and payload preview areas."""
        preview_size = get_preview_size(image)
        preview = image.resize(preview_size)
        self.preview_image = ImageTk.PhotoImage(preview)
        self.preview_label.configure(image=self.preview_image, text="")

        self.payload_preview.configure(state="normal")
        self.payload_preview.delete("1.0", "end")
        self.payload_preview.insert("1.0", payload)
        self.payload_preview.configure(state="disabled")

    def save_current_qr_code(self) -> None:
        """Save the current QR code image to a user-selected file."""
        if self.current_image is None:
            messagebox.showinfo("No QR code", "Generate a QR code first.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=(
                ("PNG image", "*.png"),
                ("JPEG image", "*.jpg;*.jpeg"),
                ("BMP image", "*.bmp"),
                ("TIFF image", "*.tif;*.tiff"),
                ("WebP image", "*.webp"),
            ),
        )
        if not path:
            return

        dpi = validate_positive_int(self.dpi_var.get(), "DPI")
        save_image(self.current_image, path, dpi=dpi)
        self.status_var.set(f"Saved: {path}")

    def print_current_qr_code(self) -> None:
        """Print the current QR code image using the Windows print action."""
        if self.current_image is None:
            messagebox.showinfo("No QR code", "Generate a QR code first.")
            return

        try:
            dpi = validate_positive_int(self.dpi_var.get(), "DPI")
            temp_path = print_image_with_windows(self.current_image, dpi=dpi)
        except OSError as exc:
            messagebox.showerror("Print failed", str(exc))
            return

        self.status_var.set(f"Print request sent: {temp_path}")
