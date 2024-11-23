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
        self.root.geometry("600x700")  # Ustawienie większego rozmiaru okna

        # Pola tekstowe dla wyrażeń z paskami przewijania
        tk.Label(root, text="Wyznaczyć:", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(root, text="(Max. 10 zmiennych decyzyjnych)", font=("Arial", 8)).pack(pady=2)
        target_frame = tk.Frame(root)
        target_frame.pack(pady=5)
        self.target_scroll = tk.Scrollbar(target_frame, orient=tk.VERTICAL)
        self.target_field = tk.Text(target_frame, height=5, width=60, font=("Arial", 10), yscrollcommand=self.target_scroll.set)
        self.target_scroll.config(command=self.target_field.yview)
        self.target_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.target_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(root, text="takie, że:", font=("Arial", 10, "bold")).pack(pady=5)
        self.optimization_type = tk.StringVar(value="")  # Przechowuje "min" lub "max"

        # Przyciski Min i Max
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        self.min_button = tk.Button(button_frame, text="Min", font=("Arial", 10), width=8,
                                    command=lambda: self.set_optimization("min"))
        self.min_button.pack(side=tk.LEFT, padx=5)
        self.max_button = tk.Button(button_frame, text="Max", font=("Arial", 10), width=8,
                                    command=lambda: self.set_optimization("max"))
        self.max_button.pack(side=tk.LEFT, padx=5)

        tk.Label(root, text="przy ograniczeniach:", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(root, text="(Max. 18 ograniczeń)", font=("Arial", 8)).pack(pady=2)
        limits_frame = tk.Frame(root)
        limits_frame.pack(pady=5)
        self.limits_scroll = tk.Scrollbar(limits_frame, orient=tk.VERTICAL)
        self.limits_field = tk.Text(limits_frame, height=10, width=60, font=("Arial", 10), yscrollcommand=self.limits_scroll.set)
        self.limits_scroll.config(command=self.limits_field.yview)
        self.limits_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.limits_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Przyciski dla operacji matematycznych
        self.create_buttons()

        # Przyciski akcji (zapis/odczyt)
        tk.Button(root, text="Zapisz do pliku", font=("Arial", 10), command=self.save_to_file).pack(pady=5)
        tk.Button(root, text="Wczytaj z pliku", font=("Arial", 10), command=self.load_from_file).pack(pady=5)

        # Przyciski dodatkowe
        tk.Button(root, text="Grupuj ograniczenia", font=("Arial", 10), command=self.group_constraints).pack(pady=5)

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

        # Resetowanie wyglądu przycisków
        self.min_button.config(bg="SystemButtonFace")
        self.max_button.config(bg="SystemButtonFace")

        # Wyróżnianie wybranego przycisku
        if opt_type == "min":
            self.min_button.config(bg="lightblue")  # Zmiana koloru tła
        elif opt_type == "max":
            self.max_button.config(bg="lightblue")

    def group_constraints(self):
        """Grupuje identyczne ograniczenia w GUI."""
        raw_constraints = self.limits_field.get("1.0", tk.END).strip()
        if not raw_constraints:
            messagebox.showinfo("Informacja", "Brak ograniczeń do grupowania.")
            return

        constraints = raw_constraints.splitlines()

        grouped = {}
        for constraint in constraints:
            match = re.match(r"(x\d+)\s*(.*)", constraint.strip())
            if match:
                variable, condition = match.groups()
                if condition not in grouped:
                    grouped[condition] = []
                grouped[condition].append(variable)
            else:
                grouped[constraint] = []

        grouped_constraints = []
        for condition, variables in grouped.items():
            if variables:
                grouped_constraints.append(f"{','.join(variables)} {condition}")
            else:
                grouped_constraints.append(condition)

        self.limits_field.delete("1.0", tk.END)
        self.limits_field.insert(tk.END, "\n".join(grouped_constraints))

        messagebox.showinfo("Sukces", "Ograniczenia zostały zgrupowane.")

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

        # Rozdziel grupowane ograniczenia na pojedyncze linie
        raw_constraints = limits.splitlines()
        expanded_constraints = []

        for constraint in raw_constraints:
            match = re.match(r"((x\d+(,x\d+)*))\s*(∈|>=|<=|>|<|=)\s*(.+)", constraint.strip())
            if match:
                variables_part, _, _, operator, condition = match.groups()
                variables_list = variables_part.split(',')
                for var in variables_list:
                    expanded_constraints.append(f"{var.strip()} {operator.strip()} {condition.strip()}")
            else:
                expanded_constraints.append(constraint.strip())

        # Walidacja ograniczeń
        invalid_constraints = []
        for constraint in expanded_constraints:
            if not re.match(r'^x\d+\s*(>=|<=|>|<|=|∈)\s*(-?\d+(\.\d+)?|R|Z|N|<[^>]*>)$', constraint.strip()):
                invalid_constraints.append(constraint)

        if invalid_constraints:
            messagebox.showerror(
                "Błąd",
                f"Następujące ograniczenia są nieprawidłowe:\n\n{', '.join(invalid_constraints)}"
            )
            return

        # Przygotowanie danych do zapisu
        expanded_limits = "\n".join(expanded_constraints)
        try:
            formatted_data = parser.format_for_file(target, optimization, expanded_limits)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się sformatować danych: {e}")
            return

        # Wybór ścieżki i zapis do pliku
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                data_handler.save_to_file(formatted_data, file_path)
                messagebox.showinfo("Sukces", "Dane zapisane do pliku!")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zapisać pliku: {e}")
    def load_from_file(self):
        """Wczytuje dane z pliku i wypełnia pola w aplikacji."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                # Pobranie danych z pliku (krotka: target, optimization, limits)
                target, optimization, limits = data_handler.load_from_file(file_path)

                constraints = limits.splitlines()
                if len(constraints) > 18:
                    messagebox.showerror("Błąd", "Plik zawiera więcej niż 18 ograniczeń.")
                    return

                # Formatowanie danych do GUI
                target_gui, optimization_gui, limits_gui = parser.format_for_gui(target, optimization, limits)

                # Wypełnienie pól w GUI
                self.target_field.delete("1.0", tk.END)
                self.limits_field.delete("1.0", tk.END)
                self.target_field.insert(tk.END, target_gui)
                self.limits_field.insert(tk.END, limits_gui)
                self.set_optimization(optimization_gui)

                messagebox.showinfo("Sukces", "Dane wczytane z pliku!")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się wczytać pliku: {e}")