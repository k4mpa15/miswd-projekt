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


def podziel_ograniczenia(ograniczenia):
    """Rozdziela ograniczenia na standardowe i specjalne."""
    standardowe_ograniczenia = []
    specjalne_ograniczenia = []

    calkowite_pattern = r"x\[(\d+)\] *E *Z"  # Pasuje do formatu x[i] E Z (liczby całkowite)

    for ograniczenie in ograniczenia:
        if re.match(calkowite_pattern, ograniczenie):
            specjalne_ograniczenia.append(ograniczenie)
        else:
            standardowe_ograniczenia.append(ograniczenie)

    return standardowe_ograniczenia, specjalne_ograniczenia
def wymus_calkowitosc(x, specjalne_ograniczenia):
    """Wymusza całkowitość zmiennych na podstawie ograniczeń."""
    calkowite_pattern = r"x\[(\d+)\] *E *Z"
    
    for ograniczenie in specjalne_ograniczenia:
        match = re.match(calkowite_pattern, ograniczenie)
        if match:
            zmienna_idx = int(match.group(1))
            x[zmienna_idx] = round(x[zmienna_idx])  # Wymuszamy całkowitość

def rozwiaz_ograniczenia_przedzialowe(ograniczenia):
    nowe_ograniczenia = []
    przedzial_pattern = r"x\[(\d+)\] *(% *\d+)? *E *< *(-?\d+) *; *(-?\d+) *>"  # Dopasowanie dla ograniczeń z przedziałami
    rzeczywiste_pattern = r"x\[(\d+)\] *E *R"  # Pasuje do formatu x[i] E R
    przedzial_5_pattern = r"(-?\d+)\s*<\s*x\[(\d+)\]\s*<\s*(-?\d+)"  # Dopasowanie dla ograniczeń typu 5 < x4 < 6
    

    for ograniczenie in ograniczenia:
        if re.match(rzeczywiste_pattern, ograniczenie):
            # Ograniczenie typu x[i] E R ignorujemy
            continue
        
        # Sprawdzamy, czy ograniczenie jest w formie 5 < x4 < 6
        match_przedzial_5 = re.match(przedzial_5_pattern, ograniczenie)
        if match_przedzial_5:
            lower_bound = float(match_przedzial_5.group(1))  # 5
            zmienna_idx = int(match_przedzial_5.group(2))  # x4
            upper_bound = float(match_przedzial_5.group(3))  # 6

            # Zamieniamy na dwa osobne ograniczenia
            nowe_ograniczenia.append(f"x[{zmienna_idx}] > {lower_bound}")
            nowe_ograniczenia.append(f"x[{zmienna_idx}] < {upper_bound}")
        else:
            match = re.match(przedzial_pattern, ograniczenie)
            if match:
                zmienna_idx = int(match.group(1))
                modulo = match.group(2)
                dolna_granica = float(match.group(3))
                gorna_granica = float(match.group(4))

                if modulo:
                    modulo_value = modulo.split('%')[1].strip()
                    nowe_ograniczenia.append(f"x[{zmienna_idx}] % {modulo_value} > {dolna_granica}")
                    nowe_ograniczenia.append(f"x[{zmienna_idx}] % {modulo_value} < {gorna_granica}")
                else:
                    nowe_ograniczenia.append(f"x[{zmienna_idx}] >= {dolna_granica}")
                    nowe_ograniczenia.append(f"x[{zmienna_idx}] <= {gorna_granica}")
            else:
                nowe_ograniczenia.append(ograniczenie)
    standardowe_ograniczenia, specjalne_ograniczenia = podziel_ograniczenia(nowe_ograniczenia)
    return standardowe_ograniczenia, specjalne_ograniczenia



def oblicz_funkcje_celu(funkcja_celu, x):
   
    
    return eval(funkcja_celu)

def wymus_ograniczenia(x, ograniczenia):
   
    for ograniczenie in ograniczenia:
        try:
            if not eval(ograniczenie):
                if "%" in ograniczenie:
                # Rozdzielanie zmiennej i reszty
                    zmienna, reszta = ograniczenie.split("%")
                    zmienna_idx = int(re.search(r"\[(\d+)\]", zmienna).group(1))

                    if "!=" in reszta:
                        modulo, wartosc = map(str.strip, reszta.split("!="))  # Usuwanie zbędnych spacji
                        modulo = int(modulo)
                        wartosc = float(wartosc)  # Zmieniamy na float
                        if x[zmienna_idx] % modulo == wartosc:
                            x[zmienna_idx] += 1  # Można tu dodać mechanizm "najbliższej wartości" jeśli chcesz

                    elif ">=" in reszta:
                        modulo, wartosc = map(str.strip, reszta.split(">="))  # Usuwanie zbędnych spacji
                        modulo = int(modulo)
                        wartosc = float(wartosc)  # Zmieniamy na float
                        # Optymalizacja: obliczamy jaką dokładnie wartość dodać, aby spełnić warunek
                        if x[zmienna_idx] % modulo < wartosc:
                            x[zmienna_idx] += (wartosc - (x[zmienna_idx] % modulo)) % modulo

                    elif "<=" in reszta:
                        modulo, wartosc = map(str.strip, reszta.split("<="))  # Usuwanie zbędnych spacji
                        modulo = int(modulo)
                        wartosc = float(wartosc)  # Zmieniamy na float
                        # Optymalizacja: obliczamy, jaką wartość odjąć, by spełnić warunek
                        if x[zmienna_idx] % modulo > wartosc:
                            x[zmienna_idx] -= (x[zmienna_idx] % modulo - wartosc) % modulo

                    elif ">" in reszta:
                        modulo, wartosc = map(str.strip, reszta.split(">"))  # Usuwanie zbędnych spacji
                        modulo = int(modulo)
                        wartosc = float(wartosc)  # Zmieniamy na float
                        # Optymalizacja: obliczamy jaką dokładnie wartość dodać, aby spełnić warunek
                        if x[zmienna_idx] % modulo <= wartosc:
                            x[zmienna_idx] += (wartosc - (x[zmienna_idx] % modulo)) % modulo

                    elif "<" in reszta:
                        modulo, wartosc = map(str.strip, reszta.split("<"))  # Usuwanie zbędnych spacji
                        modulo = int(modulo)
                        wartosc = float(wartosc)  # Zmieniamy na float
                        # Optymalizacja: obliczamy, jaką wartość odjąć, by spełnić warunek
                        if x[zmienna_idx] % modulo >= wartosc:
                            x[zmienna_idx] -= (x[zmienna_idx] % modulo - wartosc) % modulo

                    elif "==" in reszta:
                        modulo, wartosc = map(str.strip, reszta.split("=="))  # Usuwanie zbędnych spacji
                        modulo = int(modulo)
                        wartosc = float(wartosc)  # Zmieniamy na float
                        # Ustawienie zmiennej na wartość, która spełnia warunek
                        x[zmienna_idx] = x[zmienna_idx] - (x[zmienna_idx] % modulo) + wartosc

                elif ">=" in ograniczenie:
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
                elif "==" in ograniczenie:
                    zmienna, wartosc = ograniczenie.split("==")
                    zmienna_idx = int(re.search(r"\[(\d+)\]", zmienna).group(1))
                    x[zmienna_idx] = float(wartosc)
        except Exception as e:
            print(f"Błąd podczas przetwarzania ograniczenia: {ograniczenie}")
            print(f"Szczegóły błędu: {e}")
    
    return x



def solve_problem(cel, funkcja_celu, ograniczenia, n_starts=10):
    alpha = 0.01  # Współczynnik uczenia
    max_iter = 1000
    tolerance = 1e-6

    # Liczba zmiennych
    num_vars = get_variable_count(funkcja_celu, ograniczenia)
    ograniczenia, specialne_ograniczenia = rozwiaz_ograniczenia_przedzialowe(ograniczenia)

    # Minimalizacja/maksymalizacja funkcji celu
    if cel == "max":
        funkcja_celu = f"-({funkcja_celu})"

    najlepszy_wynik = float("inf") if cel == "min" else float("-inf")
    najlepsze_rozwiazanie = None

    for start in range(n_starts):
        # Losowy punkt początkowy w ograniczonym zakresie
        x = np.random.uniform(low=0, high=1, size=num_vars) * 10

        # Upewnij się, że początkowy punkt spełnia ograniczenia
        x = wymus_ograniczenia(x, ograniczenia)

        for i in range(max_iter):
            gradient = oblicz_gradient(funkcja_celu, x)
            x_new = x - alpha * gradient
            x_new = wymus_ograniczenia(x_new, ograniczenia)

            if np.linalg.norm(x_new - x) < tolerance:
                break

            x = x_new

        wynik = oblicz_funkcje_celu(funkcja_celu, x)
        wynik = -wynik if cel == "max" else wynik

        # Zapisanie najlepszego wyniku
        if (cel == "min" and wynik < najlepszy_wynik) or (cel == "max" and wynik > najlepszy_wynik):
            najlepszy_wynik = wynik
            najlepsze_rozwiazanie = x
    x = wymus_calkowitosc(x, specialne_ograniczenia)
    ograniczenia_wyniki = sprawdz_ograniczenia(najlepsze_rozwiazanie, ograniczenia, specialne_ograniczenia)

    return najlepsze_rozwiazanie, najlepszy_wynik, ograniczenia_wyniki

def sprawdz_ograniczenia(x, ograniczenia, specialne_ograniczenia):
    print(ograniczenia)
    print(specialne_ograniczenia)
    niespelnione_ograniczenia = []
    for ograniczenie in ograniczenia:
        try:
            spełnione = eval(ograniczenie)
            if not spełnione:
                niespelnione_ograniczenia.append(ograniczenie)
        except Exception as e:
            niespelnione_ograniczenia.append(f"Błąd w ograniczeniu '{ograniczenie}': {e}")
            
    for ograniczenie in specialne_ograniczenia:
        if "E Z" in ograniczenie:
            try:
                match = re.match(r"x\[(\d+)\] *E *Z", ograniczenie)
                if match:
                    zmienna_idx = int(match.group(1))
                    if not float(x[zmienna_idx]).is_integer():
                        niespelnione_ograniczenia.append(ograniczenie)
            except Exception as e:
                niespelnione_ograniczenia.append(f"Błąd w ograniczeniu '{ograniczenie}': {e}")
    wymus_ograniczenia(x, ograniczenia)            
    return niespelnione_ograniczenia




