import re

def format_for_file(target, optimization, limits):
    """
    Przygotowuje dane w formacie do zapisu w pliku.
    """
    # Konwersja funkcji celu
    target = convert_to_file_format(target)

    # Przetwarzanie ograniczeń linia po linii
    formatted_limits = []
    for line in limits.splitlines():
        line = line.strip()
        if line:
            formatted_limits.append(convert_to_file_format(line))

    # Łączenie wszystkiego w jeden ciąg znaków
    formatted_limits_str = "\n".join(formatted_limits)
    return f"{optimization} {target}\n{formatted_limits_str}"

def format_for_gui(target, optimization, limits):
    """
    Przygotowuje dane w formacie do wyświetlenia w GUI.
    """
    target = convert_to_gui_format(target)
    optimization = optimization.strip()
    limits = convert_to_gui_format(limits)
    return target, optimization, limits

def convert_to_file_format(data):
    """
    Konwertuje dane wprowadzone w GUI na format plikowy.
    """
    data = data.replace("∙", "*")
    data = data.replace("^", "**")
    data = data.replace("mod", "%")
    data = data.replace("=/=", "!=")
    data = data.replace("∧", "&&")
    data = data.replace("∨", "||")
    data = data.replace("∈", "E")

    # Obsługa zakresów w formacie <min;max>
    data = re.sub(r'<(-?\d+);(-?\d+)>', r'<\1;\2>', data)

    # Obsługa zbiorów w formacie {val1,val2,...}
    data = re.sub(r'{(-?\d+(,-?\d+)*)}', r'{\1}', data)

    # Zamiana x0! na factorial(int(x[0]))
    data = re.sub(r'x(\d+)!', r'factorial(int(x[\1]))', data)

    # Zamiana x0, x1 na x[0], x[1]
    data = re.sub(r'x(\d+)', r'x[\1]', data)

    return data.strip()

def convert_to_gui_format(data):
    """
    Zamienia dane z formatu elementarnego na format intuicyjny dla użytkownika.
    """
    data = data.replace("**", "^")
    data = data.replace("*", "∙")
    data = data.replace("%", "mod")
    data = data.replace("!=", "=/=")
    data = data.replace("&&", "∧")
    data = data.replace("||", "∨")
    data = data.replace("E", "∈")

    # Obsługa zakresów w formacie <min;max>
    data = re.sub(r'<(-?\d+);(-?\d+)>', r'<\1;\2>', data)

    # Obsługa zbiorów w formacie {val1,val2,...}
    data = re.sub(r'{(-?\d+(,-?\d+)*)}', r'{\1}', data)

    # Zamiana factorial(int(x[0])) na x0!
    data = re.sub(r'factorial\(int\(x\[(\d+)\]\)\)', r'x\1!', data)

    # Zamiana x[0], x[1] na x0, x1
    data = re.sub(r'x\[(\d+)\]', r'x\1', data)

    return data.strip()

def validate_constraints(constraints):
    """
    Waliduje ograniczenia, aby upewnić się, że mają poprawny format.
    """
    invalid_constraints = []
    for constraint in constraints.splitlines():
        constraint = constraint.strip()
        # Wzorzec dla poprawnych ograniczeń
        valid_pattern = r'^x\[\d+\]\s*(>=|<=|>|<|=|!=|%|E|\*|/|&&|\|\|)\s*.*$'
        if not re.match(valid_pattern, constraint):
            invalid_constraints.append(constraint)
    return invalid_constraints
