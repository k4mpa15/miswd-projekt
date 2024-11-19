def format_for_file(target, constraints, limits):
    """
    Zamienia dane z formatu przyjaznego dla użytkownika na format elementarny odpowiedni do zapisu w pliku.

    Args:
        target (str): Wyrażenie z sekcji "Wyznaczyć".
        constraints (str): Wyrażenie z sekcji "Takie, że".
        limits (str): Wyrażenie z sekcji "Przy ograniczeniach".

    Returns:
        str: Dane w formacie elementarnym, gotowe do zapisu w pliku.
    """
    target = convert_to_file_format(target)
    constraints = convert_to_file_format(constraints)
    limits = convert_to_file_format(limits)

    # Oddziel sekcje dwoma enterami
    return f"{target}\n\n{constraints}\n\n{limits}"


def format_for_gui(target, constraints, limits):
    """
    Zamienia dane z formatu elementarnego (plikowego) na bardziej intuicyjny dla użytkownika.

    Args:
        target (str): Wyrażenie z sekcji "Wyznaczyć" w formacie elementarnym.
        constraints (str): Wyrażenie z sekcji "Takie, że" w formacie elementarnym.
        limits (str): Wyrażenie z sekcji "Przy ograniczeniach" w formacie elementarnym.

    Returns:
        tuple: Dane w formacie intuicyjnym (target, constraints, limits).
    """
    target = convert_to_gui_format(target)
    constraints = convert_to_gui_format(constraints)
    limits = convert_to_gui_format(limits)

    return target, constraints, limits


def convert_to_file_format(data):
    """
    Konwertuje dane z formatu przyjaznego użytkownikowi na format elementarny.

    Args:
        data (str): Dane w formacie przyjaznym użytkownikowi (z GUI).

    Returns:
        str: Dane w formacie elementarnym, gotowe do zapisu w pliku.
    """
    # Symbole konwersji na format elementarny
    data = data.replace("∙", "*")
    data = data.replace(" * ", " ")
    data = data.replace("mod", "%")
    data = data.replace("=/=", "!=")
    data = data.replace("∧", "&&")
    data = data.replace("∨", "||")

    # Symbole matematyczne, pozostają niezmienione w pliku
    data = data.replace("x", "x")
    data = data.replace("Z", "Z")
    data = data.replace("R", "R")
    data = data.replace("N", "N")

    # Nawiasy i inne symbole
    data = data.replace("(", "(")
    data = data.replace(")", ")")
    data = data.replace("{", "{")
    data = data.replace("}", "}")

    return data.strip()


def convert_to_gui_format(data):
    """
    Konwertuje dane z formatu elementarnego (plikowego) na bardziej intuicyjny dla użytkownika.

    Args:
        data (str): Dane w formacie elementarnym (z pliku).

    Returns:
        str: Dane w formacie przyjaznym użytkownikowi, gotowe do wyświetlenia w GUI.
    """
    # Symbole konwersji na format przyjazny użytkownikowi
    data = data.replace("*", "∙")
    data = data.replace(" ", " * ")
    data = data.replace("%", "mod")
    data = data.replace("!=", "=/=")
    data = data.replace("&&", "∧")
    data = data.replace("||", "∨")

    # Symbole matematyczne, pozostają niezmienione w GUI
    data = data.replace("x", "x")
    data = data.replace("Z", "Z")
    data = data.replace("R", "R")
    data = data.replace("N", "N")
    # Nawiasy i inne symbole
    data = data.replace("(", "(")
    data = data.replace(")", ")")
    data = data.replace("{", "{")
    data = data.replace("}", "}")

    return data.strip()
