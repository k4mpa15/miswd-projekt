import tkinter as tk
from tkinter import filedialog, messagebox
import parser
import data_handler

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Konwerter równań")

        # Pola tekstowe
        tk.Label(root, text="Wyznaczyć:").pack()
        self.target_field = tk.Text(root, height=3, width=50)
        self.target_field.pack()

        tk.Label(root, text="takie, że:").pack()
        self.constraints_field = tk.Text(root, height=3, width=50)
        self.constraints_field.pack()

        tk.Label(root, text="przy ograniczeniach:").pack()
        self.limits_field = tk.Text(root, height=10, width=50)
        self.limits_field.pack()

        # Przyciski operacji matematycznych
        self.create_buttons()

        # Przyciski akcji
        tk.Button(root, text="Zapisz do pliku", command=self.save_to_file).pack()
        tk.Button(root, text="Wczytaj z pliku", command=self.load_from_file).pack()

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()

        buttons = [
            ("Dodaj +", "+"), ("Odejmij -", "-"), ("Mnożenie *", "*"), ("Dzielenie /", "/"),
            ("Modulo %", "%"), ("Potęga **", "**"), ("Mniejsze <", "<"),
            ("Mniejsze równe <=", "<="), ("Większe >", ">"), ("Większe równe >=", ">="),
            ("Nierówne =!=", "!="), ("Zawiera się E", " E "), ("Nie zawiera \\", " \\ "),
            ("AND", " && "), ("OR", " || ")
        ]

        for text, operator in buttons:
            tk.Button(frame, text=text, command=lambda op=operator: self.insert_operator(op)).pack(side=tk.LEFT)

    def insert_operator(self, operator):
        # Wstawienie operatora w aktywne pole tekstowe
        active_widget = self.root.focus_get()
        if isinstance(active_widget, tk.Text):
            active_widget.insert(tk.INSERT, operator)

    def save_to_file(self):
        # Pobranie danych z pól tekstowych
        target = self.target_field.get("1.0", tk.END).strip()
        constraints = self.constraints_field.get("1.0", tk.END).strip()
        limits = self.limits_field.get("1.0", tk.END).strip()

        # Parsowanie danych i zapis do pliku
        formatted_data = parser.format_data(target, constraints, limits)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            data_handler.save_to_file(formatted_data, file_path)
            messagebox.showinfo("Sukces", "Dane zapisane do pliku!")

    def load_from_file(self):
        # Wczytanie danych z pliku
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            content = data_handler.load_from_file(file_path)
            if content:
                target, constraints, limits = content
                self.target_field.delete("1.0", tk.END)
                self.constraints_field.delete("1.0", tk.END)
                self.limits_field.delete("1.0", tk.END)

                self.target_field.insert(tk.END, target)
                self.constraints_field.insert(tk.END, constraints)
                self.limits_field.insert(tk.END, limits)
                messagebox.showinfo("Sukces", "Dane wczytane z pliku!")
