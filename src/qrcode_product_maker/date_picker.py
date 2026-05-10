"""Gregorian calendar widgets and date helpers."""

import calendar
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Callable


MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


@dataclass(frozen=True)
class SelectedDate:
    """A user-selected Gregorian date."""

    year: int
    month: int
    day: int

    def display_value(self) -> str:
        """Return the date formatted for showing in the form and QR payload."""
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"


class DateInput(ttk.Frame):
    """A compact date input with a picker button."""

    def __init__(self, master: tk.Misc, label: str) -> None:
        """Create the date input."""
        super().__init__(master)
        self.label_text = label
        self.value_var = tk.StringVar()

        self.columnconfigure(0, weight=1)
        self.entry = ttk.Entry(self, textvariable=self.value_var, state="readonly")
        self.entry.grid(row=0, column=0, sticky="ew")

        pick_button = ttk.Button(self, text="Pick", command=self.open_picker)
        pick_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        clear_button = ttk.Button(self, text="Clear", command=self.clear)
        clear_button.grid(row=0, column=2, sticky="ew", padx=(6, 0))

    def get(self) -> str:
        """Return the selected date text or an empty string."""
        return self.value_var.get().strip()

    def clear(self) -> None:
        """Clear the selected date."""
        self.value_var.set("")

    def open_picker(self) -> None:
        """Open the calendar picker window."""
        DatePickerDialog(master=self.winfo_toplevel(), on_select=self._set_selected_date)

    def _set_selected_date(self, selected_date: SelectedDate) -> None:
        """Store the selected date in the input field."""
        self.value_var.set(selected_date.display_value())


class DatePickerDialog(tk.Toplevel):
    """Popup date picker for Gregorian dates."""

    def __init__(
        self,
        master: tk.Misc,
        on_select: Callable[[SelectedDate], None],
    ) -> None:
        """Create a date picker dialog."""
        super().__init__(master)
        self.title("Select date")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.on_select = on_select
        self.year_var = tk.IntVar(value=2026)

        self._build()
        self._refresh_days()

    def _build(self) -> None:
        """Build picker controls."""
        frame = ttk.Frame(self, padding=14)
        frame.grid(row=0, column=0, sticky="nsew")

        controls = ttk.Frame(frame)
        controls.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        controls.columnconfigure(1, weight=1)

        ttk.Label(controls, text="Year").grid(row=0, column=0, padx=(0, 6))
        year_spin = ttk.Spinbox(
            controls,
            from_=1900,
            to=2100,
            textvariable=self.year_var,
            width=8,
            command=self._refresh_days,
        )
        year_spin.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        year_spin.bind("<KeyRelease>", lambda _event: self._refresh_days())

        ttk.Label(controls, text="Month").grid(row=0, column=2, padx=(0, 6))
        self.month_combo = ttk.Combobox(controls, values=MONTH_NAMES, state="readonly", width=14)
        self.month_combo.current(0)
        self.month_combo.grid(row=0, column=3, sticky="ew")
        self.month_combo.bind("<<ComboboxSelected>>", self._on_month_changed)

        weekdays = ttk.Frame(frame)
        weekdays.grid(row=1, column=0, sticky="ew")
        for column, label in enumerate(WEEKDAY_LABELS):
            ttk.Label(weekdays, text=label, anchor="center", width=5).grid(row=0, column=column)

        self.days_frame = ttk.Frame(frame)
        self.days_frame.grid(row=2, column=0, sticky="nsew")

    def _on_month_changed(self, _event: object) -> None:
        """Refresh days after the month changes."""
        self._refresh_days()

    def _refresh_days(self) -> None:
        """Draw the day grid for the current month and year."""
        for child in self.days_frame.winfo_children():
            child.destroy()

        year = self._safe_year()
        month = self.month_combo.current() + 1 if hasattr(self, "month_combo") else 1
        first_weekday, month_length = calendar.monthrange(year, month)

        for day in range(1, month_length + 1):
            index = first_weekday + day - 1
            row = index // 7
            column = index % 7
            button = ttk.Button(
                self.days_frame,
                text=str(day),
                width=5,
                command=lambda selected_day=day: self._select_day(selected_day),
            )
            button.grid(row=row, column=column, padx=2, pady=2)

    def _safe_year(self) -> int:
        """Return a valid year from the spinbox value."""
        try:
            return int(self.year_var.get())
        except tk.TclError:
            return 2026

    def _select_day(self, day: int) -> None:
        """Select the clicked day and close the dialog."""
        selected = SelectedDate(
            year=self._safe_year(),
            month=self.month_combo.current() + 1,
            day=day,
        )
        self.on_select(selected)
        self.destroy()
