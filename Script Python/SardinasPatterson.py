############
## IMPLEMENTAZIONE ALGORITMO DI SARDINAS-PATTERSON ##
############

"""
Un Codice è UD se ogni sequenza di Codewords corrisponde al più a una sequenza di simboli della sorgente.

Prima di procedere con l'implementazione ricordiamo che l'Algoritmo si basa sul seguente teorema:

Sia C il codice, si considerino dei sottoinsiemi nella forma S_i dove:
S_0 = C
S_i = {w in A* t.c. esiste 'a' in S_0 ed esiste 'b' in S_i-1 tali che a = bw oppure b = aw}

Vale a dire, l'i-esimo insieme è costruito, a partire dal precedente, in modo tale che questo contenga tutte
le words che sono suffisse di una word 'a' in S_0 oppure suffisse di una word 'b' in S_i-1

Il Codice è UD se per ogni n > 0 abbiamo che l'intersezione di S_0 e S_n è l'insieme vuoto.
"""

# Funzione che crea l'insieme n-esimo
def create_set_n(code, n):
    if n == 0:
        return set(code)

    else:
        set_n = set()

        # Poichè S_n è creato a patire da S_0 ed S_n-1, chiamo ricorsivamente la funzione per creare
        # il set precedente
        previous_set = create_set_n(code, n-1)

        # Per ogni codeword dell'insieme S_0 verifico se esiste una word nell'insieme S_n-1 tale per cui
        # questa è un prefisso della suddetta codeword.
        # Se ciò accade, aggiungo all'insieme S_n la word w tale per cui a = bw
        for a in code:
            for b in previous_set:

                # Attraverso la funzione find verifico che venga trovato, all'interno di 'a', 
                # il pattern composto dalla stringa 'b' e che questo cominci proprio alla
                # prima posizione della word 'a'; ovvero, verifico che 'b' sia prefisso di tutta la
                # stringa 'a'.
                if (len(a) > len(b) and a.find(b) == 0):

                    # Aggiungo a S_n la parte della word 'a' che comincia a partire dalla posizione
                    # successiva all'ultimo simbolo della word 'b'
                    set_n.add(a[len(b):])

        # Per ogni word dell'insieme S_n-1 verifico se esiste una codeword nell'insieme S_0 tale per cui
        # questa è un suo suffisso; ovvero, verifico se la codeword è un prefisso per la word di S_n-1.
        # Se ciò accade, aggiungo all'insieme S_n la word w tale per cui b = aw
        for b in previous_set:
            for a in code:
                if(len(b) > len(a) and b.find(a) == 0):
                    
                    # Aggiungo a S_n la parte della word 'b' che comincia a partire dalla posizione 
                    # successiva all'ultimo simbolo della word 'a'
                    set_n.add(b[len(a):])

        return set_n

"""
Funzione che costruisce l'insieme unione di tutti gli insiemi generati fino al criterio di stop.
In generale, abbiamo tre criteri di stop differenti:

1) Per qualche n S_0 intersezione S_n != void --> Codice non UD
2) Per qualche i > 0 abbiamo che S_i = void (e così gli insiemi successivi)
3) Per qualche i, j > 0 abbiamo che S_i = S_j e si entra in un loop

Vogliamo, dunque, fare in modo che gli insiemi vengano generato fino a quando non si raggiunge uno
dei criteri.
"""

def create_all_sets(code):
    list_of_sets = []
    last_set = set()

    # Comincio a generare gli insiemi a partire da S_1 (Dato che S_0 = Code)
    n = 1
    current_set = create_set_n(code, n)

    # Verifico se S_n è un insieme vuoto, fermandomi qualora fosse tale

    while(len(current_set) > 0):

        # Se l'insieme generato è già presente tra gli insiemi già costruiti mi fermo.
        if current_set in list_of_sets:
            break

        else:
            list_of_sets.append(current_set)

            # Aggiorno il contenuto di last_set con l'unione tra questo e l'insieme appena generato
            last_set = last_set.union(current_set)

            n += 1

            current_set = create_set_n(code, n)

    # Infine restituisco l'insime contenente tutti i suffissi 'w' generati
    return last_set

"""
Funzione che applica l'Algoritmo di Sardinas-Patterson utilizzando le funzioni definite sopra.
In particolare, si inserisce in input un Codice il quale verrà suddiviso in tutte le sue Codewords,
formando un insieme.
Verrà chiamata la funzione "create_all_sets" che restituirà l'insieme contenente tutte le words 'w'
suffisse delle Codewords del Codice.
Infine, si verificherà se l'intersezione tra il Codice e il suddetto insieme formerà l'insieme vuoto (Caso UD)
oppure no (Caso NON UD).
"""
def sardinas_patterson():

    code_string = input('Inserisci le codewords separate da spazio\n')

    codewords = code_string.split(' ')

    code = set(codewords)

    last_set = create_all_sets(code)

    if (len(code.intersection(last_set)) == 0):
        print("\nIl Codice proposto è UD\n")
    else:
        print("\nCodice non UD\n")

