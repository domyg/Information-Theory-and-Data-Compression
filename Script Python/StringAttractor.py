from LZEncoding import lz77_variant_encoding as lz77
from LZEncoding import compute_runs as runs
from LZEncoding import BWT, BWT_LF, compute_LF

############
## IMPLEMENTAZIONE VERIFICA STRING ATTRACTOR ##
############

def generate_substring(T):

    subs = []

    # Genero l'insieme di tutte le possibili sottostringhe di 'T'
    for i in range(0, len(T)):
        for j in range(i, len(T)):
            if T[i:j+1] not in subs:
                subs.append((T[i:j+1]))
    
    return subs


# Gamma è String Attractor di T se ogni sottostringa 'sub', presente in T, ha un'occorrenza 
# nel testo 'T' che è delimitata dagli indici 'i' e 'j' tali da contenere un indice 'j_k'
# che appartiene a Gamma
# N.B. Gli indici cominciano da '0'

def isAttractor(T: str, Gamma):

    # Genero, innanzitutto, l'insieme di tutte le possibili sottostringhe di T
    subs = generate_substring(T)

    dict = {}

    # Per ogni sottostringa generata, ne conto le occorrenze e, per ognuna di queste, memorizzo gli indici
    # che la delimitano all'interno del testo 'T'
    for sub in subs:
        sub_count = T.count(sub)
        indexes = []
        start = 0
        end = 0

        # Itero tra le occorrenze di 'sub' in 'T' e, per ognuna, calcolo l'indice iniziale e quello che segue
        # immediatamente tale occorrenza
        for i in range(sub_count):
            start = T.index(sub, end)
            end = start + len(sub)
            
            # Tramite questo ciclo aggiungo il valore degli indici compresi tra 'start' ed 'end' che
            # delimitano la i-esima occorrenza della sottostringa nel testo 'T'

            for j in range(start, end):
                indexes.append(str(j))
        

        # Sfrutto un dizionario per memorizzare tutti gli indici che compongono 'sub' nel testo 'T'
        dict[sub] = indexes

    # Estraggo le chiavi del dizionario; ovvero, estraggo la lista di sottostringhe individuate
    keys = dict.keys()

    is_attractor = True

    # Per ogni sottostringa memorizzata nel dizionario, verifico se esiste un range di indici tale da 
    # contenere almeno uno tra gli indici 'j_k' di Gamma 
    for k in keys:
        check = False
        for g in Gamma:
            if str(g) in dict[k]:
                check = True

            if check == True:
                break

        # Gamma è uno String Attractor se, per ogni sottostringa 'k', esiste una coppia di indici che ne
        # delimita un'occorrenza tale per cui 'g' appartiene al range delimitato da tale coppia
        is_attractor = is_attractor and check

        # Se per una qualunque sottosringa 'k' la suddetta condizione non dovesse verificarsi
        # si potrebbe concludere che la sequenza proposta non è uno String Attractor per il testo T
        if not is_attractor:
            break

    return is_attractor


def find_attractor_lz77(T):

    # Sfrutto la funzione definita nel file 'LZEncoding.py' la quale restituisce in output una codifica
    # del testo, effettuata con una variante LZ77 che produce coppie (start_index, length), e una lista
    # contenente gli indici che identificano l'ultimo carattere di ogni sottostringa a partire da cui
    # è stata generata una frase LZ77
    lz77_enc, positions = lz77(T)

    Gamma = positions
    if isAttractor(T, Gamma):
        return Gamma
    
    else:
        return []


# Dal paper "String Attractors and Combinatorics on Words" di:
# S. Mantaci, A. Restivo, G. Romana, G. Rosone, M. Sciortino
"""
In particular, in the proof of Theorem 1 the string attractor is constructed by
considering the position of the symbols in w that correspond, in the output of the
transformation, to the first occurrence of a symbol in each run (or, equivalently,
the last occurrence of a symbol in each run).
"""

# Gamma_BWT sarà composto dall'insieme delle posizioni alla fine delle run di lettere uguali trovate in BWT(T)
# N.B. Questa implementazione comporta problemi in quanto non riesce a individuare uno String Attractor per
# il testo 'abaababaabaab'
def find_attractor_bwt_1(T):
    Gamma = []
    L, I = BWT(T)
    Gamma = runs(L, SA = True)
    print(str(Gamma))

    if isAttractor(T, Gamma):
        return Gamma
    else:
        return []
    

# Dal paper "At the Roots of Dictionary Compression: String Attractors" di D. Kempa ed N. Prezza:
"""
'Consider the process of inverting the BWT to obtain T.
The inversion algorithm is based on the observation that T [n - k] = L[LF^k [p0]]
for k ∈ [0, n - 1], where p0 is the position of T [n] in L.
From the formula for LF it is easy to see that if two positions i, j belong to the same equal-letter run in L
then LF[j] = LF[i] + (j - i).
Let Gamma_BWT = {n - k | LF^k[p0] = 1 or L[LF^k[p0] - 1] !=L[LF^k[p0]]}'
"""

# Gamma_BWT, dunque, sarà formato da tutte quelle posizioni (n-k) tali per cui:
# LF^k[p_0] = 1  OPPURE  L[LF^k[p_0] - 1] != L[LF^k[p_0]]
# Dove p_0 è la posizione di T[n] in L (Ovvero I)
# N.B. Questa implementazione comporta problemi in quanto non restituisce alcuno String Attractor per
# il testo 'adcbaadcbadc'
def find_attractor_bwt_2(T):

    Gamma = []
    L, I = BWT(T)

    LF = BWT_LF(L)

    n  = len(T) - 1
    p_0 = I

    for k in range(n):
        if (compute_LF(LF, p_0, k) == 1) or (L[compute_LF(LF, p_0, k) - 1] != L[compute_LF(LF, p_0, k)]):
            Gamma.append(n-k)

    if isAttractor(T, Gamma):
        return sorted(Gamma)
    else:
        return []


# Una Finite Sturmian Word non è altro che un fattore di una Sturmian Word
# Una Finite Sturmian Word è costruita a partire da una sequenza di numeri naturali d_0, ..., d_n tale
# per cui d_0 >= 0 e d_i > 0 per ogni i = 1 ... n

# Una Finite Sturmian Word è una qualsiasi sequenza S_n tale per cui S_0 = b, S_1 = a, S_(n+1) = S_n^dn S_(n-1)
# Si può provare che le Sturmian Words Finite hanno come String Attractor minimo quello composto da due
# posizioni consecutive.


# Funzione che individua lo String Attractor minimo per un testo T
"""def find_min_attractor(T):

    candidates = []
    for i in range(len(T)):
        candidates.append([i])

    for c in candidates:
        tmp = c
        if isAttractor(T,tmp):
            continue

        for i in range(len(T)):
            tmp.append(i)
            if isAttractor(tmp):
                break"""


    #print(str(candidates))


# Passo allo svolgimento del successivo esercizio di portfolio
# Non mi è chiaro come continuare lo svolgimento di quello corrente


def string_attractor_menu():
    print("\nBenvenut* nel menù riguardante gli String Attractor!\n")

    while True:
        print("\n\
            1) String Attractor Checking\n\
            2) LZ77 String Attractor\n\
            3) BWT String Attractor (Presenta Problemi)\n\
            4) Exit")
        sel = input("Seleziona cosa fare: ")

        if sel == '1':
            x = input("Inserisci la stringa:\n")
            y = input("Inserisci le posizioni nello String Attractor separate dallo spazio ' '\n")

            Gamma = y.split()
            check = isAttractor(x, Gamma)

            if check:
                print("\nString Attractor Valido!")
            else:
                print("\nLo String Attractor inserito non è valido")

        elif sel == '2':
            x = input("Inserisci la stringa:\n")

            Gamma = find_attractor_lz77(x)

            print("\nLo String Attractor identificato è il seguente:")
            print(str(Gamma))

        elif sel == '3':
            x = input("Inserisci Stringa:\n")

            Gamma1 = find_attractor_bwt_1(x)
            Gamma2 = find_attractor_bwt_2(x)

            print("\
                  Nonostante l'Algoritmo presenta alcuni problemi (descritti nei commenti del codice),\n\
                  verranno presentati due String Attractor possibili (non necessariamente corretti)\n\
                  generati a partire da due Algoritmi differenti\n")
            print(str(Gamma1))
            print("\n\n")
            print(str(Gamma2))

        elif sel == '4':
            break
