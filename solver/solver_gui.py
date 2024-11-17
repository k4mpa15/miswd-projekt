import tkinter as tk
from tkinter import filedialog
from solver import process_data, solve_problem

cel = None
funkcja_celu = None
ograniczenia = None

def get_file():
    global cel, funkcja_celu, ograniczenia
    path = filedialog.askopenfilename(filetypes=[("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")])
    if path:
        try:
            with open(path, 'r') as file:
                data = file.read()

            cel, funkcja_celu, ograniczenia = process_data(data)

            eq_text.delete(1.0, tk.END)
            eq_text.insert(tk.END, f"Funkcja celu:\n{funkcja_celu} ---> {cel}\n")
            eq_text.insert(tk.END, "\n".join(ograniczenia))
            solve_button.config(state=tk.NORMAL)

        except Exception as e:
            eq_text.delete(1.0, tk.END)
            eq_text.insert(tk.END, f"Błąd wczytywania pliku: {e}")

def solve():
    global cel, funkcja_celu, ograniczenia
    x, wynik = solve_problem(cel, funkcja_celu, ograniczenia)
    solution_text.insert(tk.END, f"Rozwiązanie: {x}\n")
    solution_text.insert(tk.END, f"Funkcja celu: {wynik}\n")

def erase():
    solution_text.delete(1.0, tk.END)

root = tk.Tk()
root.title("Solver")

get_file_button = tk.Button(root, text="Wczytaj plik", command=get_file)
get_file_button.pack(pady=10)

solve_button = tk.Button(root, text="Rozwiąż równanie", command=solve, state=tk.DISABLED)
solve_button.pack(pady=10)

erase_button = tk.Button(root, text="Wyczyść", command=erase)
erase_button.pack(pady=10)

eq_text = tk.Text(root, width=150, height=15)
eq_text.pack(pady=10)

solution_text = tk.Text(root, width=150, height=15)
solution_text.pack(pady=10)

root.mainloop()
