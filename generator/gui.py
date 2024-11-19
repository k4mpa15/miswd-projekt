import tkinter as tk
from tkinter import filedialog, messagebox
import parser
import data_handler
import re


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Konwerter Równań")

        # Ustawienia ogólne rozmiaru
        self.root.geometry("500x600")  # Ustawienie mniejszego rozmiaru okna

        # Pola tekstowe dla wyrażeń
        tk.Label(root, text="Wyznaczyć:", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(root, text="(Max. 10 zmiennych decyzyjnych)", font=("Arial", 8)).pack(pady=2)
        self.target_field = tk.Text(root, height=2, width=40, font=("Arial", 10))
        self.target_field.pack(pady=5)

        tk.Label(root, text="takie, że:", font=("Arial", 10, "bold")).pack(pady=5)
        self.optimization_type = tk.StringVar(value="")  # Przechowuje "min" lub "max"

        # Przyciski Min i Max
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Min", font=("Arial", 10), width=8,
                  command=lambda: self.set_optimization("min")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Max", font=("Arial", 10), width=8,
                  command=lambda: self.set_optimization("max")).pack(side=tk.LEFT, padx=5)

        tk.Label(root, text="przy ograniczeniach:", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(root, text="(Min. 15 ograniczeń)", font=("Arial", 8)).pack(pady=2)
        self.limits_field = tk.Text(root, height=8, width=40, font=("Arial", 10))
        self.limits_field.pack(pady=5)

        # Przyciski dla operacji matematycznych
        self.create_buttons()

        # Przyciski akcji (zapis/odczyt)
        tk.Button(root, text="Zapisz do pliku", font=("Arial", 10), command=self.save_to_file).pack(pady=5)
        tk.Button(root, text="Wczytaj z pliku", font=("Arial", 10), command=self.load_from_file).pack(pady=5)

    def create_buttons(self):
        """Tworzy przyciski z symbolami matematycznymi w układzie 5x5."""
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        buttons = [
            ("{", "{"), ("}", "}"), ("x", "x"), ("(", "("), (")", ")"),
            ("+", "+"), ("-", "-"), ("∙", "∙"), ("\\", " \\ "), ("^", "^"),
            ("!", "!"), ("*", " * "), ("mod", " mod "), ("=/=", "=/="), ("=", "="),
            ("<", "<"), ("<=", "<="), (">", ">"), (">=", ">="), ("∈", " ∈ "),
            ("∧", " ∧ "), ("∨", " ∨ "), ("R", "R"), ("Z", "Z"), ("N", "N")
        ]

        for row in range(5):  # Liczba wierszy
            for col in range(5):  # Liczba kolumn
                idx = row * 5 + col
                if idx < len(buttons):
                    text, value = buttons[idx]
                    btn = tk.Button(
                        frame, text=text, width=4, height=1, font=("Arial", 9, "bold"),
                        command=lambda val=value: self.insert_text(val)
                    )
                    btn.grid(row=row, column=col, padx=2, pady=2)

    def set_optimization(self, opt_type):
        """Ustawia typ optymalizacji na 'min' lub 'max'."""
        self.optimization_type.set(opt_type)

    def insert_text(self, value):
        """Wstawia tekst (symbol operacji) do aktywnego pola tekstowego."""
        active_widget = self.root.focus_get()
        if isinstance(active_widget, tk.Text):
            active_widget.insert(tk.INSERT, value)

    def save_to_file(self):
        """Zapisuje dane do pliku w odpowiednim formacie."""
        target = self.target_field.get("1.0", tk.END).strip()
        optimization = self.optimization_type.get().strip()
        limits = self.limits_field.get("1.0", tk.END).strip()

        if not optimization:
            messagebox.showerror("Błąd", "Wybierz typ (Min lub Max).")
            return

        # Weryfikacja liczby zmiennych decyzyjnych
        variables = re.findall(r'x\d+', target)  # Szuka zmiennych decyzyjnych w funkcji celu
        if len(set(variables)) > 10:
            messagebox.showerror("Błąd", "Funkcja celu może zawierać maksymalnie 10 zmiennych decyzyjnych.")
            return

        # Weryfikacja liczby ograniczeń
        constraints = limits.splitlines()
        if len(constraints) < 15:
            messagebox.showerror("Błąd", "Musisz wprowadzić co najmniej 15 ograniczeń.")
            return

        formatted_data = parser.format_for_file(target, optimization, limits)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            data_handler.save_to_file(formatted_data, file_path)
            messagebox.showinfo("Sukces", "Dane zapisane do pliku!")

    def load_from_file(self):
        """Wczytuje dane z pliku i wypełnia pola w aplikacji."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            content = data_handler.load_from_file(file_path)
            if content:
                target, optimization, limits = parser.format_for_gui(*content)
                self.target_field.delete("1.0", tk.END)
                self.limits_field.delete("1.0", tk.END)

                self.target_field.insert(tk.END, target)
                self.optimization_type.set(optimization)
                self.limits_field.insert(tk.END, limits)
                messagebox.showinfo("Sukces", "Dane wczytane z pliku!")
