import string

############
## IMPLEMENTAZIONE ALGORITMO RE-PAIR ##
############


# Funzione che costruisce una Codifica del testo 'T' basata sulle Grammatiche Context-Free
def repair_enc(T: str, lower=False, n_char = 0):

    # Opzione che impone il lowercase di tutti i caratteri del testo
    if lower:
        T = T.lower()

    # Sfrutto un dizionario contenente coppie (Non-Teminale - Terminale)
    dict = {}

    # Fino alla condizione di 'break', che avviene solo quando non si trovano più coppie di simboli adiacenti
    # con più di 1 occorrenza, costruisco il dizionario e vado sostituendo le coppie di Simboli con maggiore
    # frequenza con dei nuovi simboli Non Terminali
    while True:

        pair_freq = {}

        # Costurisco un dizionario contenente, per ogni coppia di simboli adiacenti presenti nel testo,
        # la rispettiva frequenza di occorrenza senza sovrapposizioni
        for i in range(0,len(T)-1):

            pair = T[i] + T[i+1]
            pair_freq[pair] = T.count(pair)

        # Trovo la coppia con maggiori occorrenze
        max_pair = max(pair_freq, key=pair_freq.get)

        # Se la coppia con maggior frequenza ha al più un'occorrenza è arrivato il momento di fermarsi
        if pair_freq[max_pair] <= 1:
            break
        
        # Creo un Simbolo Non Terminale unico da utilizzare per rappresentare la coppia appena trovata
        NT = string.ascii_uppercase[n_char]

        # Rimpiazzo la coppia 'max_pair' con il nuovo simbolo 'NT'
        T = T.replace(max_pair, NT)

        # Aggiungo al Dizionario la coppia Chiave - Valore che rappresenta la sostituzione della coppia
        # di simboli adiacenti più frequente con un Simbolo Non Terminale
        dict[NT] = max_pair

        n_char += 1

    return T, dict

# Funzione che, a partire da una Stringa e da una Grammatica, riesce a decodificare la Stringa
# codificata con RE-PAIR
def repair_dec(enc_T: str, dict: dict):

    # Sfrutto il dizionario inverso così da decodificare prima gli ultimi Simboli Non Terminali inseriti
    for k in list(reversed(dict.keys())):
        enc_T = enc_T.replace(k, dict[k])
    
    return enc_T

# Funzione che effettua una codifica con RE-PAIR costruendo la Grammatica nella CNF
def repair_cnf(T: str):
    
    # Prendo i singoli simboli che compongono la stringa 'T' di input e li sostituisco con dei Simboli
    # Non Terminali
    symbols = T.strip()
    symbols = list(sorted(set(symbols)))
    NT_symbols = {}
    n_char = 0
    for s in symbols:
        NT = string.ascii_uppercase[n_char]
        NT_symbols[NT] = s
        n_char += 1
        
        # Rimpiazzio i simboli Terminali nella stringa di input con i nuovi Non Terminali
        T = T.replace(s, NT)
    
    # Sfrutto l'algoritmo RE-PAIR fornendo come parametro 'n_char' l'i-esimo carattere ASCII upper_case da
    # cui cominciare a formare i nuovi Non Terminali
    T, dict = repair_enc(T, n_char = n_char)

    # Effettuo il merge dei due dizionari per costruire l'intera Grammatica CNF
    dict = NT_symbols | dict

    return T, dict


def repair_menu():

    print("Benvenut* nel Menù di RE-PAIR\n")

    while True:
        print("\n\
              1) RE-PAIR Encoding\n\
              2) RE-PAIR Encoding with CNF Grammar\n\
              3) Exit\n")
        sel = input("Seleziona cosa fare: ")

        if sel == '1':
            x = input("Seleziona la stringa da Codificare:\n")

            T, G = repair_enc(x)
            keys = G.keys()

            for k in keys:
                print("\n|" + str(k) + "->" + str(G[k]))

            print("\nLa stringa codificata con la suddetta Grammatica è la seguente:\n" + T)

            print("\n-----\n")
            print("La corrispettiva Decodifica è la seguente:\n")
            dec = repair_dec(T, G)
            print(str(dec))

        elif sel == '2':
            x = input("Seleziona la stringa da Codificare con una Grammatica CNF: \n")

            T, G_cnf = repair_cnf(x)
            keys = G_cnf.keys()

            for k in keys:
                print("\n|" + str(k) + "->" + str(G_cnf[k]))

            print("\nLa stringa codificata con la suddetta Grammatica CNF è la seguente:\n" + T)

            print("\n-----\n")
            print("La corrispettiva Decodifica è la seguente:\n")
            dec = repair_dec(T, G_cnf)
            print(str(dec))

        elif sel == '3':
            break

