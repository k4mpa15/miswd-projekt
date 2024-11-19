import tkinter as tk
from tkinter import filedialog, messagebox
import parser
import data_handler


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Konwerter Równań")

        # Pola tekstowe dla wyrażeń
        tk.Label(root, text="Wyznaczyć:", font=("Arial", 12, "bold")).pack(pady=5)
        self.target_field = tk.Text(root, height=3, width=50, font=("Arial", 12))
        self.target_field.pack(pady=5)

        tk.Label(root, text="takie, że:", font=("Arial", 12, "bold")).pack(pady=5)
        self.constraints_field = tk.Text(root, height=3, width=50, font=("Arial", 12))
        self.constraints_field.pack(pady=5)

        tk.Label(root, text="przy ograniczeniach:", font=("Arial", 12, "bold")).pack(pady=5)
        self.limits_field = tk.Text(root, height=10, width=50, font=("Arial", 12))
        self.limits_field.pack(pady=5)

        # Przyciski dla operacji matematycznych
        self.create_buttons()

        # Przyciski akcji (zapis/odczyt)
        tk.Button(root, text="Zapisz do pliku", font=("Arial", 12), command=self.save_to_file).pack(pady=5)
        tk.Button(root, text="Wczytaj z pliku", font=("Arial", 12), command=self.load_from_file).pack(pady=5)

    def create_buttons(self):
        """Tworzy przyciski z symbolami matematycznymi w układzie 5x5."""
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Operacje, które mają być obsługiwane
        buttons = [
            # Rząd 1
            ("{", "{"), ("}", "}"), ("x", "x"), ("(", "("), (")", ")"),
            # Rząd 2
            ("+", "+"), ("-", "-"), ("∙", "∙"), ("\\", " \\ "), ("^", "^"),
            # Rząd 3
            ("!", "!"), ("*", " * "), ("mod", " mod "), ("=/=", "=/="), ("=", "="),
            # Rząd 4
            ("<", "<"), ("<=", "<="), (">", ">"), (">=", ">="), ("∈", " ∈ "),
            # Rząd 5
            ("∧", " ∧ "), ("∨", " ∨ "), ("R", "R"), ("Z", "Z"), ("N", "N")
        ]

        # Tworzenie siatki przycisków
        for row in range(5):  # Liczba wierszy
            for col in range(5):  # Liczba kolumn
                idx = row * 5 + col
                if idx < len(buttons):
                    text, value = buttons[idx]
                    btn = tk.Button(
                        frame, text=text, width=5, height=2, font=("Arial", 10, "bold"),
                        command=lambda val=value: self.insert_text(val)
                    )
                    btn.grid(row=row, column=col, padx=3, pady=3)

    def insert_text(self, value):
        """Wstawia tekst (symbol operacji) do aktywnego pola tekstowego."""
        active_widget = self.root.focus_get()
        if isinstance(active_widget, tk.Text):
            active_widget.insert(tk.INSERT, value)

    def save_to_file(self):
        """Zapisuje dane do pliku w odpowiednim formacie."""
        target = self.target_field.get("1.0", tk.END).strip()
        constraints = self.constraints_field.get("1.0", tk.END).strip()
        limits = self.limits_field.get("1.0", tk.END).strip()

        # Konwersja na format elementarny
        formatted_data = parser.format_for_file(target, constraints, limits)
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
                # Konwersja na format przyjazny użytkownikowi
                target, constraints, limits = parser.format_for_gui(*content)
                self.target_field.delete("1.0", tk.END)
                self.constraints_field.delete("1.0", tk.END)
                self.limits_field.delete("1.0", tk.END)

                self.target_field.insert(tk.END, target)
                self.constraints_field.insert(tk.END, constraints)
                self.limits_field.insert(tk.END, limits)
                messagebox.showinfo("Sukces", "Dane wczytane z pliku!")
