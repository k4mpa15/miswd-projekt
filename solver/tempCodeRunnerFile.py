    alpha = 0.01  # Współczynnik uczenia
    max_iter = 1000  # Maksymalna liczba iteracji
    tolerance = 1e-6  # Tolerancja zbieżności
    x = np.random.rand(7) * 10  # Początkowe wartości zmiennych 

    for i in range(max_iter):
        # Obliczanie gradientu i aktualizacja zmiennych
        gradient = oblicz_gradient(x)
        x_new = x - alpha * gradient

        # Naprawianie zmiennych, aby spełniały ograniczenia
        x_new = wymus_ograniczenia(x_new)

        # Sprawdzanie, czy różnica jest wystarczająco mała (zbieżność)
        if np.linalg.norm(x_new - x) < tolerance:
            break

        # Aktualizacja zmiennych
        x = x_new

    solution_text.insert(tk.END, f"\nRozwiązanie: {x}\n")
    solution_text.insert(tk.END, f"Funkcja celu: {oblicz_funkcje_celu(x)}\n")