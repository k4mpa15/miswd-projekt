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
            algorithm_1_button.config(state=tk.NORMAL)
            algorithm_2_button.config(state=tk.NORMAL)
            algorithm_3_button.config(state=tk.NORMAL)

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
    eq_text.delete(1.0, tk.END)

root = tk.Tk()
root.title("Solver")
root.geometry("800x600")  

root.configure(bg="#2E2E2E")  

get_file_button = tk.Button(
    root, 
    text="Wczytaj plik", 
    command=get_file, 
    bg="#4A90E2", 
    fg="white", 
    activebackground="#357ABD", 
    activeforeground="white",
    relief="flat",
    padx=10,
    pady=5
)
get_file_button.pack(pady=10)

algorithm_frame = tk.Frame(root, bg="#2E2E2E")
algorithm_frame.pack(pady=10)

algorithm_1_button = tk.Button(
    algorithm_frame, 
    text="Metoda najmniejszego spadku", 
    command=solve, 
    bg="#4A90E2", 
    fg="white", 
    activebackground="#357ABD", 
    activeforeground="white",
    relief="flat",
    padx=10,
    pady=5
)
algorithm_1_button.pack(side=tk.LEFT, padx=5)

algorithm_2_button = tk.Button(
    algorithm_frame, 
    text="Algorytm 2", 
    command=solve, 
    bg="#4A90E2", 
    fg="white", 
    activebackground="#357ABD", 
    activeforeground="white",
    relief="flat",
    padx=10,
    pady=5
)
algorithm_2_button.pack(side=tk.LEFT, padx=5)

algorithm_3_button = tk.Button(
    algorithm_frame, 
    text="Algorytm 3", 
    command=solve, 
    bg="#4A90E2", 
    fg="white", 
    activebackground="#357ABD", 
    activeforeground="white",
    relief="flat",
    padx=10,
    pady=5
)
algorithm_3_button.pack(side=tk.LEFT, padx=5)

algorithm_4_button = tk.Button(
    algorithm_frame, 
    text="Algorytm 4", 
    command=solve, 
    bg="#4A90E2", 
    fg="white", 
    activebackground="#357ABD", 
    activeforeground="white",
    relief="flat",
    padx=10,
    pady=5
)
algorithm_4_button.pack(side=tk.LEFT, padx=5)

spacer = tk.Frame(algorithm_frame, bg="#2E2E2E", width=200)
spacer.pack(side=tk.LEFT, fill=tk.Y)

erase_button = tk.Button(
    algorithm_frame, 
    text="Wyczyść", 
    command=erase, 
    bg="#4A90E2", 
    fg="white", 
    activebackground="#357ABD", 
    activeforeground="white",
    relief="flat",
    padx=10,
    pady=5
)
erase_button.pack(side=tk.RIGHT, padx=7)

eq_text = tk.Text(root, width=150, height=15, bg="#1E1E1E", fg="white", insertbackground="white", bd=0)
eq_text.pack(pady=10)

solution_text = tk.Text(root, width=150, height=15, bg="#1E1E1E", fg="white", insertbackground="white", bd=0)
solution_text.pack(pady=10)

root.mainloop()