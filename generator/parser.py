def format_for_file(target, optimization, limits):
    """
    Przygotowuje dane w formacie do zapisu w pliku.
    """
    target = convert_to_file_format(target)
    optimization = convert_to_file_format(optimization)
    limits = convert_to_file_format(limits)
    return f"{target}\n\n{optimization}\n\n{limits}"


def format_for_gui(target, optimization, limits):
    """
    Przygotowuje dane w formacie do wyświetlenia w GUI.
    """
    target = convert_to_gui_format(target)
    optimization = convert_to_gui_format(optimization)
    limits = convert_to_gui_format(limits)
    return target, optimization, limits


def convert_to_file_format(data):
    """
    Zamienia dane wprowadzone w GUI na format elementarny.
    """
    data = data.replace("∙", "*")
    data = data.replace(" * ", " ")
    data = data.replace("mod", "%")
    data = data.replace("=/=", "!=")
    data = data.replace("∧", "&&")
    data = data.replace("∨", "||")
    data = data.replace("!", "!")
    data = data.replace("=", "=")
    data = data.replace("x", "x")
    data = data.replace("Z", "Z")
    data = data.replace("R", "R")
    data = data.replace("N", "N")
    data = data.replace("(", "(")
    data = data.replace(")", ")")
    data = data.replace("{", "{")
    data = data.replace("}", "}")
    return data.strip()


def convert_to_gui_format(data):
    """
    Zamienia dane z formatu elementarnego na format intuicyjny dla użytkownika.
    """
    data = data.replace("*", "∙")
    data = data.replace(" ", " * ")
    data = data.replace("%", "mod")
    data = data.replace("!=", "=/=")
    data = data.replace("&&", "∧")
    data = data.replace("||", "∨")
    data = data.replace("!", "!")
    data = data.replace("=", "=")
    data = data.replace("x", "x")
    data = data.replace("Z", "Z")
    data = data.replace("R", "R")
    data = data.replace("N", "N")
    data = data.replace("(", "(")
    data = data.replace(")", ")")
    data = data.replace("{", "{")
    data = data.replace("}", "}")
    return data.strip()
