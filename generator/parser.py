def format_data(target, constraints, limits):
    """
    Formatuje dane zgodnie z ustalonymi zasadami.
    """
    # Usuwamy nadmiarowe spacje, wstawiamy indeksy dla zmiennych x
    target = process_equations(target)
    constraints = process_equations(constraints)
    limits = process_equations(limits)

    # Rozdzielenie sekcji dwoma spacjami
    return f"{target}  {constraints}  {limits}"

def process_equations(data):
    """
    Przetwarza równania, zamieniając zmienne na indeksowane oraz operatorami na właściwe formatowanie.
    """
    import re

    # Zamiana x1 -> x[1]
    data = re.sub(r'\bx(\d+)\b', r'x[\1]', data)

    # Zamiana operatorów na właściwy format
    data = data.replace("**", "^")
    data = data.replace("&&", " and ")
    data = data.replace("||", " or ")
    data = data.replace("=!=", "≠")
    data = data.replace("<=", "≤")
    data = data.replace(">=", "≥")
    data = data.replace("\\", "∉")
    data = data.replace("E", "∈")

    return data.strip()
