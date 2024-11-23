def save_to_file(data, file_path):
    """
    Zapisuje dane do pliku w ustalonym formacie.
    """
    try:
        with open(file_path, "w") as file:
            file.write(data)
    except Exception as e:
        raise IOError(f"Błąd zapisu do pliku: {e}")


def load_from_file(file_path):
    """
    Wczytuje dane z pliku w formacie elementarnym.
    """
    try:
        with open(file_path, "r") as file:
            content = file.read().strip()

        # Podziel plik na pierwszą linię (funkcja celu z optymalizacją) i resztę (ograniczenia)
        lines = content.splitlines()
        if len(lines) < 2:
            raise ValueError("Niepoprawny format pliku. Oczekiwano funkcji celu oraz ograniczeń.")

        # Pierwsza linia: "min/max <funkcja celu>"
        first_line = lines[0]
        if not first_line.startswith(("min", "max")):
            raise ValueError("Niepoprawny format pierwszej linii. Oczekiwano 'min' lub 'max'.")

        # Rozdziel "min/max" od funkcji celu
        optimization, target = first_line.split(maxsplit=1)

        # Pozostałe linie to ograniczenia
        limits = "\n".join(lines[1:])

        # Zwraca dane jako krotkę
        return (target, optimization, limits)
    except Exception as e:
        raise IOError(f"Błąd wczytywania pliku: {e}")