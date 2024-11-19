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
            content = file.read()

        # Podział na sekcje (dwie linie przerwy)
        sections = content.split("\n\n")
        if len(sections) != 3:
            raise ValueError("Niepoprawny format pliku. Oczekiwano trzech sekcji oddzielonych dwiema liniami przerwy.")

        target = sections[0].strip()
        constraints = sections[1].strip()
        limits = sections[2].strip()

        return target, constraints, limits
    except Exception as e:
        raise IOError(f"Błąd wczytywania pliku: {e}")
