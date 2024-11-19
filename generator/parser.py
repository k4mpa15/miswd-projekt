def format_for_file(target, constraints, limits):
    target = convert_to_file_format(target)
    constraints = convert_to_file_format(constraints)
    limits = convert_to_file_format(limits)
    return f"{target}\n\n{constraints}\n\n{limits}"


def format_for_gui(target, constraints, limits):
    target = convert_to_gui_format(target)
    constraints = convert_to_gui_format(constraints)
    limits = convert_to_gui_format(limits)
    return target, constraints, limits


def convert_to_file_format(data):
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
