def validate_input(equations):
    lines = equations.split("\n")
    if len(lines) < 15:
        return False  # Minimum 15 constraints required
    for line in lines:
        if not line.strip():
            continue
        if len(set(line).intersection(set("0123456789x[]+-*/%^<>=!&|"))) == 0:
            return False
    return True
