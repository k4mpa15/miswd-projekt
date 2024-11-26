import re

def format_for_file(target, optimization, limits):
    """
    Przygotowuje dane w formacie do zapisu w pliku.
    """
    target = convert_to_file_format(target)
    optimization = optimization.strip()
    limits = convert_to_file_format(limits)
    return f"{optimization} {target}\n{limits}"


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
    Zamienia dane wprowadzone w GUI na format elementarny.
    """
    data = data.replace("∙", "*")
    data = data.replace("^", "**")
    data = data.replace("mod", "%")
    data = data.replace("=/=", "!=")
    data = data.replace("∧", "&&")
    data = data.replace("∨", "||")
    data = data.replace("∈", "E")

    # Zamiana x3! na factorial(int(x[3]))
    data = re.sub(r'x(\d+)!', r'factorial(int(x[\1]))', data)

    # Zamiana x0, x1, ... na x[0], x[1], ...
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

    # Zamiana factorial(int(x[3])) na x3!
    data = re.sub(r'factorial\(int\(x\[(\d+)\]\)\)', r'x\1!', data)

    # Zamiana x[0], x[1], ... na x0, x1, ...
    data = re.sub(r'x\[(\d+)\]', r'x\1', data)
    return data.strip()