import re
import numpy as np
import math  

def get_variable_count(funkcja_celu, ograniczenia):
    pattern = r"x\[(\d+)\]"  
    all_matches = re.findall(pattern, funkcja_celu)  
    for ograniczenie in ograniczenia:
        all_matches.extend(re.findall(pattern, ograniczenie))  
    unique_indices = sorted(set(map(int, all_matches)))  
    return max(unique_indices) + 1  

def process_data(data):
    linie = data.strip().split("\n")
    pierwsza_linia = linie[0].split(" ")

    cel = pierwsza_linia[0]  
    funkcja_celu = pierwsza_linia[1]  

    ograniczenia = []
    for linia in linie[1:]:
        ograniczenie = linia.strip()
        if ograniczenie:
            ograniczenia.append(ograniczenie)

    return cel, funkcja_celu, ograniczenia

def oblicz_gradient(funkcja_celu, x):
    gradient = np.zeros_like(x)
    h = 1e-6  
    for i in range(len(x)):
        x_forward = x.copy()
        x_forward[i] += h
        f_forward = oblicz_funkcje_celu(funkcja_celu, x_forward)

        x_backward = x.copy()
        x_backward[i] -= h
        f_backward = oblicz_funkcje_celu(funkcja_celu, x_backward)

        gradient[i] = (f_forward - f_backward) / (2 * h)
    return gradient

def rozwiaz_ograniczenia_przedzialowe(ograniczenia):
    nowe_ograniczenia = []
    przedzial_pattern = r"x\[(\d+)\] *E *< *(-?\d+) *; *(-?\d+) *>"  

    for ograniczenie in ograniczenia:
        match = re.match(przedzial_pattern, ograniczenie)
        if match:
            zmienna_idx = int(match.group(1))
            dolna_granica = float(match.group(2))
            gorna_granica = float(match.group(3))

            nowe_ograniczenia.append(f"x[{zmienna_idx}] >= {dolna_granica}")
            nowe_ograniczenia.append(f"x[{zmienna_idx}] <= {gorna_granica}")
        else:
            nowe_ograniczenia.append(ograniczenie)

    return nowe_ograniczenia

def oblicz_funkcje_celu(funkcja_celu, x):
    x_int = np.array([int(val) if val.is_integer() else val for val in x])
    lokalny_kontekst = {"x": x_int, "factorial": math.factorial, "math": math}
    return eval(funkcja_celu, {"__builtins__": None}, lokalny_kontekst)

def wymus_ograniczenia(x, ograniczenia):
    x_int = np.array([int(val) if val.is_integer() else val for val in x])
    for ograniczenie in ograniczenia:
        lokalny_kontekst = {"x": x_int, "factorial": math.factorial, "math": math}
        if not eval(ograniczenie, {"__builtins__": None}, lokalny_kontekst):
            if ">=" in ograniczenie:
                zmienna, wartosc = ograniczenie.split(">=")
                zmienna_idx = int(re.search(r"\[(\d+)\]", zmienna).group(1))
                x[zmienna_idx] = max(x[zmienna_idx], float(wartosc))
            elif "<=" in ograniczenie:
                zmienna, wartosc = ograniczenie.split("<=")
                zmienna_idx = int(re.search(r"\[(\d+)\]", zmienna).group(1))
                x[zmienna_idx] = min(x[zmienna_idx], float(wartosc))
            elif "<" in ograniczenie:
                zmienna, wartosc = ograniczenie.split("<")
                zmienna_idx = int(re.search(r"\[(\d+)\]", zmienna).group(1))
                x[zmienna_idx] = min(x[zmienna_idx], float(wartosc) - 1e-6)
            elif ">" in ograniczenie:
                zmienna, wartosc = ograniczenie.split(">")
                zmienna_idx = int(re.search(r"\[(\d+)\]", zmienna).group(1))
                x[zmienna_idx] = max(x[zmienna_idx], float(wartosc) + 1e-6)
            elif "!=" in ograniczenie:
                zmienna, wartosc = ograniczenie.split("!=")
                zmienna_idx = int(re.search(r"\[(\d+)\]", zmienna).group(1))
                if abs(x[zmienna_idx] - float(wartosc)) < 1e-6:
                    x[zmienna_idx] += 1e-6
            elif "mod" in ograniczenie:
                zmienna, reszta = ograniczenie.split("mod")
                zmienna_idx = int(re.search(r"\[(\d+)\]", zmienna).group(1))

                if "!=" in reszta:
                    modulo, wartosc = map(int, reszta.split("!="))
                    if x[zmienna_idx] % modulo == wartosc:
                        x[zmienna_idx] += 1  
                elif ">=" in reszta:
                    modulo, wartosc = map(int, reszta.split(">="))
                    while x[zmienna_idx] % modulo < wartosc:
                        x[zmienna_idx] += 1
                elif "<=" in reszta:
                    modulo, wartosc = map(int, reszta.split("<="))
                    while x[zmienna_idx] % modulo > wartosc:
                        x[zmienna_idx] -= 1
                elif ">" in reszta:
                    modulo, wartosc = map(int, reszta.split(">"))
                    while x[zmienna_idx] % modulo <= wartosc:
                        x[zmienna_idx] += 1
                elif "<" in reszta:
                    modulo, wartosc = map(int, reszta.split("<"))
                    while x[zmienna_idx] % modulo >= wartosc:
                        x[zmienna_idx] -= 1
                elif "==" in reszta:
                    modulo, wartosc = map(int, reszta.split("=="))
                    x[zmienna_idx] = x[zmienna_idx] - (x[zmienna_idx] % modulo) + wartosc
    return x


def solve_problem(cel, funkcja_celu, ograniczenia):
    alpha = 0.01  # Współczynnik uczenia
    max_iter = 1000
    tolerance = 1e-6
    x = np.random.rand(get_variable_count(funkcja_celu, ograniczenia)) * 10

    if cel == "max":
        funkcja_celu = f"-({funkcja_celu})" 

    ograniczenia = rozwiaz_ograniczenia_przedzialowe(ograniczenia)

    for i in range(max_iter):
        gradient = oblicz_gradient(funkcja_celu, x)
        x_new = x - alpha * gradient
        x_new = wymus_ograniczenia(x_new, ograniczenia)

        if np.linalg.norm(x_new - x) < tolerance:
            break

        x = x_new

    wynik = oblicz_funkcje_celu(funkcja_celu, x)
    return x, -wynik if cel == "max" else wynik
