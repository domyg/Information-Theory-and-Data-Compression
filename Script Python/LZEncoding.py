############
## IMPLEMENTAZIONE ALGORITMI DI COMPRESSIONE BASATI SU DIZIONARI ##
############

import random
import string
import matplotlib.pyplot as plt
import math


def lz77_encoding(text, W=20):

    output = []

    # Inizializzo i Buffer di Ricerca e di LookAhead
    search = ''
    look_ahead = ''

    # Inizializzo l'indice che identifica il carattere di input da scansionare
    current = 0


    while current < len(text):

        # Suddivido, a ogni iterazione, i due Buffer sulla base dell'indice del carattere di input
        # da scansionare al passo corrente
        # Considero, inoltre, una Sliding Window 'W' che limita la lunghezza del Buffer di Ricerca
        search = text[max(0, current - W):current]
        look_ahead = text[current:]

        # Inizializzo una Stringa 'subs' che conterrà la Sottostringa corrente da usare per la ricerca nel
        # dizionario
        subs = ''

        # 'length' e 'offset' sono delle variabili utilizzate per riempire i valori delle Terzine di output
        length = 0
        offset = 0

        # La terzina viene inizializzata considerando la creazione di una terzina senza referenziare
        # alcuna sottostringa del Search Buffer
        triplet = (0, 0, look_ahead[0])


        # La ricerca della sottostringa viene fatta considerando la sua presenza all'interno del Search Buffer
        # all'aumentare dei caratteri scansionati dal Look Ahead Buffer
        for c in look_ahead[:len(look_ahead)-1]:
            subs += c
            if subs not in search:
                subs = subs[0:len(subs)-1]
                break

        length = len(subs)

        # Se la sottostringa ha lunghezza pari a 0, e quindi non esiste, l'output prodotto sarà la Terzina
        # iniziale e il valore dell'indice 'current' verrà incrementato di 1, passando alla scansione
        # successiva
        if length == 0:
            output.append(triplet)
            current += 1
            continue

        # Sfrutto una variabile di controllo e un indice contatore per verificare la ripetizione
        # della sottostringa nel LookAhead Buffer
        end_check = True
        index = 0

        # Questo ciclo verifica se la sottostringa trovata si ripete, anche in parte, fino al penultimo
        # carattere del LookAhead Buffer
        for i in range(len(look_ahead)-1):
            if index % length == 0:
                index = 0

            # Se almeno un carattere di 'subs' differisce da un carattere di 'look_ahead',
            # oppure se subs non termina alla fine del Search Buffer, il controllo fallisce
            # e imposta a False il contenuto di 'end_check'
            if ((subs[index] != look_ahead[i]) or (search[-length:] != subs)):
                end_check = False
                break
            index += 1


        # Qualora la sottostringa riuscisse a ripetersi fino al penultimo carattere del LookAhead Buffer,
        # il valore di lunghezza della Terzina verrebbe incrementato considerando il numero di caratteri
        # della sottostringa che si ripetono fino ad arrivare al penultimo carattere del Buffer di LookAhead.
        if end_check:
            length += index
            
        # Utilizzo il metodo 'rfind' per individuare in quale parte del testo ha inizio
        # la sottostringa, cominciando a cercare questa dalla fine del Search Buffer
        start_index = str(search).rfind(subs)

        # 'offset' indica la distanza del carattere di inizio della sottostringa rispetto al carattere
        # corrente
        offset = len(search) - start_index - 1

        # Se la lunghezza della sottostringa del dizionario è inferiore a quella del Buffer di LookAhead,
        # vorrà dire che la scansione continuerà e, quindi, che il carattere della Terzina
        # non corrisponderà all'ultimo del testo
        if offset < len(search) and length < len(look_ahead):
            triplet = (offset + 1, length, look_ahead[length])

        # Se la lunghezza della sottostringa non è inferiore a quella del Buffer di LookAhead, vorrà dire
        # che questa sarà l'ultima scansione e che, quindi, la Terzina stamperà sicuramente
        # l'ultimo carattere del Buffer di LookAhead.
        # Se la lunghezza della sottostringa è maggiore rispetto a quella del Buffer di LookAhead
        # sarà necessario sottrarre il valore di 'index' a 'length'.
        # Di fatto, se la sottostringa si ripetesse, questa assumerebbe un valore di 'index' tale per cui
        # 'length' + 'index' < len('look_ahead')
        elif offset < len(search):
            triplet = (offset + 1, length-index, look_ahead[len(look_ahead)-1])
        
        output.append(triplet)
        
        # Aggiorno il valore della variabile contenente l'indice del nuovo carattere da scansionare
        # considerando che avrò scansionato un numero di caratteri pari alla lunghezza della sottostringa
        # e un ulteriore carattere che corrisponde a quello immediatamente successivo alla suddetta
        current += triplet[1] + 1


    # Restituisco la Lista contenente tutte le Terzine che rappresentano la Codifica LZ77
    return output


def lz77_decoding(triplets):

    output = ''
    subs = ''

    # Scandisco la lista delle terzine, salvando i valori correnti <o, l, s>
    for t in triplets:

        offset = t[0]
        length = t[1]
        symbol = t[2]

        # Se l'offset della sottostringa rappresentata dalla terzina è pari a zero vorrà dire
        # che la terzina rappresenta solamente il simbolo nel terzo elemento della stessa, quindi potrò
        # concatenarlo all'output
        if offset == 0:
            output += symbol

        else:
            # Strutturo la sottostringa prendendo la parte di output indicata dall'offset e limitata
            # al valore di lunghezza della Terzina
            subs = output[-offset : len(output) - offset + length]

            # Qualora il valore di offset fosse inferiore a quello di lunghezza vorrebbe dire che
            # la sottostringa si ripete per formare i caratteri decifrati
            if offset < length:
                index = 0

                # Tramite questo ciclo iterativo stampo in output i caratteri della sottostringa, considerando
                # anche quelli che si ripetono
                for i in range(length):
                    if index % len(subs) == 0:
                        index = 0
                    output += subs[index]
                    index += 1

            else:
                output += subs
            
            # Infine, a prescindere dalla sottostringa, aggiungerò all'output il simbolo indicato nella
            # Terzina
            output += symbol

    return output


def lzss_encoding(text, W=20):

    output = []

    search = ''
    look_ahead = ''

    current = 0

    while current < len(text):

        search = text[max(0, current - W):current]
        look_ahead = text[current:]

        subs = ''

        offset = 0
        length = 0

        # Nonostante l'implementazione sia analoga a quella di LZ77,
        # LZss prevede in output delle coppie piuttosto che delle terzine
        pair = (0, look_ahead[0])

        # In questo caso itero lungo tutto il Buffer di LookAhead in quanto non è necessario lasciare
        # un carattere extra da includere nella Coppia
        for c in look_ahead[:len(look_ahead)]:
            subs += c
            if subs not in search:
                subs = subs[0:len(subs)-1]
                break
        
        length = len(subs)

        if length == 0:
            output.append(pair)
            current += 1
            continue

        end_check = True
        index = 0

        for i in range(len(look_ahead)):
            if index % length == 0:
                index = 0

            if ((subs[index] != look_ahead[i]) or (search[-length:] != subs)):
                end_check = False
                break

            index += 1

        if end_check:
            length += index

        
        start_index = str(search).rfind(subs)

        offset = len(search) - start_index - 1

        if offset < len(search) and length <= len(look_ahead):
            pair = (offset + 1, length)

        elif offset < len(search):
            pair = (offset + 1, length - index)

        
        output.append(pair)

        current += pair[1]
    
    return output


def lzss_decoding(pairs):

    output = ''
    subs = ''

    for pair in pairs:
        offset = pair[0]
        length_char = pair[1]

        if offset == 0:
            output += length_char
        
        else:
            subs = output[-offset : len(output) - offset + length_char]

            if offset < length_char:
                index = 0
                for i in range(length_char):
                    if index % len(subs) == 0:
                        index = 0
                    output += subs[index]
                    index += 1

            else:
                output += subs

    return output


# Questa variante è definita per essere utilizzata durante lo costruzione di uno String Attractor,
# considerando che il numero di frasi generate da LZ77, per un certo testo, è pari alla cardinalità
# di uno String Attractor ammissibile per lo stesso.
# Inoltre, codificando il testo con la seguente variante, basterà comporre lo String Attractor con gli
# indici che indicano la posizione nel testo di ogni simbolo finale delle frasi LZ77 generate 
def lz77_variant_encoding(text: str):

    output = []

    # Lista contenente l'insieme delle posizioni alla fine di ogni frase LZ77
    positions = []
    current = 0

    while current < len(text):

        # Testo da analizzare
        scan_text = text[current:]
        subs = ''

        index = 0
        length = 0

        last_position = 0

        pair = (0, scan_text[0])

        for c in scan_text:
            subs += c
            if subs not in text[:current]:
                subs = subs[0:len(subs)-1]
                break

        length = len(subs)

        if length == 0:
                output.append(pair)
                positions.append(current)
                current += 1
                continue
        
        # Memorizzo l'indice di inizio della sottostringa trovata all'interno del testo analizzato
        # fino al momento corrente
        index = text[:current].index(subs)

        # La coppia, in questa variante, contiene l'indice 'i' per cui T[i]
        # corrisponde al primo carattere della sottostringa
        pair = (index, length)

        output.append(pair)

        current += pair[1]

        # 'last_position' corrisponde alla posizione in 'T' dell'ultimo carattera della sottostringa
        # appena utilizzata
        last_position = current - 1
        positions.append(last_position)

    return output, positions


def BWT(text):

    # Dichiaro una lista che conterrà tutte le rotazioni del Testo effettuate dalla BWT
    rot = []

    for i in range(len(text)):
        # Aggiungo alla lista di rotazioni quelle generate facendo variare l'indice 'i'
        # che indica l'indice iniziale della rotazione corrente
        rot.append(text[i:] + text[:i])

    # Riordino tutte le permutazioni del testo originale
    sorted_rot = sorted(rot)
    L = ''
    I = 0

    for i in range(len(text)):
        # Creo la stringa 'L' che rappresenta l'ultima colonna della Tabella contenente le rotazioni ordinate
        L += sorted_rot[i][len(text)-1]
        if sorted_rot[i] == text:
            I = i
    
    # Ritorno la colonna 'L' e l'indice corrispondente alla riga che contiene il testo originale
    return L, I


# Questa funzione è di supporto per la costruzione della Matrice 'Tau' (Ovvero LF) che è rappresentata
# come un Array.
def BWT_LF(L):
    
    # Per prima cosa si costruisce F ordinando la stringa L
    F = ''.join(sorted(L))
    LF = []
    j = 0
    used_indexes = []
    
    # Per ogni carattere in F trovo la prima occorrenza dello stesso all'interno di L salvando la coppia
    # di indici (In realtà salvo solo l'indice di L dato che l'indice di F corrisponderà alla
    # i-esima entry dell'Array che viene costruito)
    for i in range(len(L)):
        j = 0
        char = F[i]
        while j < len(L):
            if char == L[j] and j not in used_indexes:
                # Memorizzo gli indici di L già utilizzati al fine di non considerare più quelle occorrenze
                used_indexes.append(j)
                LF.append(j)
                j += 1
                break
            j += 1

    return LF


# Funzione di supporto per calcolare le potenze di LF[x]
def compute_LF(LF, x, k):

    output = 0

    if k == 0:
        output = x
    else:
        output = LF[compute_LF(LF, x, k-1)]

    return output


# Funzione ausiliaria che restituisce una lista, di dimensione pari al numero di run di lettere uguali,
# delle run di simboli consecutivi con le lunghezze a esse associate
def compute_runs(bwt_text, SA = False):
    
    output = []

    length = len(bwt_text)
    i = 0
    j = 0

    # Insieme delle posizioni nel testo relative agli ultimi caratteri di ogni run individuata
    indexes = []

    # Per ogni carattere del testo verifico se i successivi sono uguali a quello corrente
    while i < length - 1:
        count = 0
        char = bwt_text[i]
        j = i + 1

        # Variabile che utilizzo per memorizzare, per ogni run, l'indice del simbolo finale di questa.
        # L'utilità verrà mostrata nell'implementazione di uno String Attractor, per un testo T, sfruttando
        # proprio le run presenti in BWT(T)
        last_run_index = length - 1

        # Itero lungo il testo di input fintantoché trovo dei caratteri che sono uguali al carattere corrente
        while j < length:
            if char == bwt_text[j]:
                count += 1
                j += 1
            
            # Al primo carattere differente che incontro interrompo l'iterazione lungo il testo
            elif char != bwt_text[j]:
                last_run_index = j - 1
                break
        
        indexes.append(last_run_index)

        # Inserisco nella lista di output il carattere corrente analizzato e la lunghezza della rispettiva run
        output.append((char, count+1))

        # Faccio partire l'iterazione seguente dal primo carattere diverso da quello che ha formato la run
        # precedente
        i = j
    if SA:
        return indexes
    else:
        return output, len(output)


def compare_triplets_runs(S=10,E=100):
    
    number_77 = []
    number_ss = []
    number_bwt = []
    f_z77= []
    f_zss = []
    f_r = []

    # A ogni iterazione costruisco un testo casuale composto da 'i' simboli che verrà codificato dai
    # diversi metodi al fine di generare le differenti triple/runs
    for i in range(S,E+1):
        text = ''.join(random.choices(string.ascii_lowercase, k=i))

        # Effettuo le singole codifiche e ne memorizzo le lunghezze
        LZ77 = lz77_encoding(text)
        z77 = len(LZ77)

        LZss = lzss_encoding(text)
        zss = len(LZss)

        # Per la BWT, effettuo la trasformazione del testo (BWT(T)) e calcolo il numero di runs presenti
        # nell'output della trasformazione
        L, I = BWT(text)
        runs, r = compute_runs(L)
        
        n = len(text)

        # Creo delle liste contenenti le suddette lunghezze per cui l'indice 'i' in cui esse sono contenute
        # corrisponde al valore ('S' + 'i'), ovvero la lunghezza del testo codificato
        number_77.append(z77)
        number_ss.append(zss)
        number_bwt.append(r)

        # Creo delle funzioni utili a effettuare degli esperimenti
        f_z77.append(z77 * math.pow(math.log2(n), 2))
        f_zss.append(zss * math.pow(math.log2(n), 2))
        f_r.append(r * math.log2(n))
    
    # Verifico se le due condizioni seguenti sono rispettate
    # r = O(z log^2 n)
    # z = O(r log n)

    # f(x) = O(g(x)) se esiste una costante positiva 'c' e un numero reale X_0 tale per cui
    # f(x) <= c*g(X) per ogni X >= X_0
            
    cz = 1
    cr = 1

    # Verificando z = O(r log n) se ne dimostra la veridicità per un qualuqnue valore di 'c' >= 1.
    # Di fatto, z non crescerà mai più velocemente di (r log n) e, dunque, (r log n) è un Upper Bound per z
    # VEDERE GRAFICO 1
    for i in range(len(f_r)):
        f_r[i] *= cz
    
    # Verificando r = O(z log^2 n) si nota come la condizione è sempre rispettata in quanto
    # r cresce sempre meno velocemente di (z log^2 n) e, dunque, (z log^2 n) è un Upper Bound per r
    # VEDERE GRAFICO 2
    for i in range(len(f_z77)):
        f_z77[i] *= cr

    # Creo dei Grafici per riportare i risultati dei vari esperimenti
    plt.plot(range(S,E+1), number_77, label = "LZ77")
    plt.plot(range(S,E+1), number_ss, label = "LZss")
    plt.plot(range(S,E+1), number_bwt, label = "BWT")
    plt.legend()
    plt.title('Comparison between N° of Triplets/Pairs and Equal-Letter Runs')
    plt.ylabel('Number of Triplets/Pairs/Runs')
    plt.xlabel('Text Length')
    plt.show()

    plt.plot(range(S,E+1), number_77, label = "LZ77")
    plt.plot(range(S,E+1), number_ss, label = "LZss")
    plt.plot(range(S,E+1), f_r, label = "(r log n)")
    plt.title('z = O(r log n)')
    plt.ylabel('Number of Triplets/Pairs/Runs')
    plt.xlabel('Text Length')
    plt.legend()
    plt.show()

    plt.plot(range(S,E+1), f_z77, label = "(z log^2 n)")
    plt.plot(range(S,E+1), number_ss, label = "LZss")
    plt.plot(range(S,E+1), number_bwt, label = "BWT")
    plt.title('r = O(z log^2 n)')
    plt.ylabel('Number of Triplets/Pairs/Runs')
    plt.xlabel('Text Length')
    plt.legend()
    plt.show()


def ex_1(k, i):

    output = ''

    # Costruisco l'insieme delle concatenazioni delle words 'ab^j^k' al variare di 'j' con 'k' fissato
    for j in range(1, i+1):
        set = ['a', 'b'*(j**k)]
        set = ''.join([str(item) for item in set])
        output += set

    L, I = BWT(output)
    runs, r = compute_runs(L)
    z = len(lz77_encoding(output))

    return 'r = ' + str(r) + '  |  z = ' + str(z)


# Creo una funzione ausiliaria che ritorna la sequenza delle parole di Fibonacci fino alla i-esima.
# In particolare, le words di Fibonacci sono formate a partire da un qualunque alfabeto binario e sono
# calcolate allo stesso modo dei numeri di Fibonacci, concatenando tra loro la word n-1 ed n-2
def get_fibonacci_words(i):

    words = []

    j = 1

    words = ['a', 'ab']
    
    while j < i:
        words.append(words[j] + words[j - 1])
        j = j + 1

    return words


def ex_2(i):
    
    fib_words = get_fibonacci_words(i)

    odd_fib = ''

    # Considero le sole Word di Fibonacci con indice Dispari
    for i in range(len(fib_words)):
        if i % 2 == 0:
            continue
        odd_fib += fib_words[i]

    L, I = BWT(odd_fib)
    runs, r = compute_runs(L)
    z = len(lz77_encoding(odd_fib))

    return 'r = ' + str(r) + '  |  z = ' + str(z)


def ex_3(i):
    
    fib_words = get_fibonacci_words(i)

    even_fib = ''

    # Considero le sole word di Fibonacci con indice Pari
    for i in range(len(fib_words)):
        if i % 2 == 0:
            even_fib += fib_words[i]

    L, I = BWT(even_fib)
    runs, r = compute_runs(L)
    z = len(lz77_encoding(even_fib))

    return 'r = ' + str(r) + '  |  z = ' + str(z)


def ex_4(k=6):

    output = ''

    # Costruisco una prima parte dell'insieme 'output' concatenando tra loro le stringhe:
    # s_i = (ab^(i)aa) ed e_i = (ab^(i)aba(i-2)) al variare di 'i' tra 2 e 'k'.
    for i in range(2,k):
        s = ['a', 'b'*i, 'a', 'a']
        e = ['a', 'b'*i, 'a', 'b', 'a'*(i-2)]
        s = ''.join([str(item) for item in s])
        e = ''.join([str(item) for item in e])
        output += s+e

    # Infine, concatenerò all'output un'ultima stringa q = (ab^(k)a)
    q = ['a', 'b'*k, 'a']
    q = ''.join([str(item) for item in q])
    output += q

    L, I = BWT(output)
    runs, r = compute_runs(L)
    z = len(lz77_encoding(output))

    return 'r = ' + str(r) + '  |  z = ' + str(z)


def lz_coding_menu():

    print("\nBenvenut* nel menù riguardante la Codifica basata su Dizionari!\n")

    while True:
        print("\n\
            1) LZ77 Encoding\n\
            2) LZss Encoding\n\
            3) BWT\n\
            4) Esperimenti\n\
            5) Exit\n")
        
        sel = input("Seleziona cosa fare: ")

        if sel == '1':
            x = input("Inserisci il testo da codificare: ")
            print("\n")
            W = input("Inserisci la dimensione della Sliding Window (Premi Invio per Default): ")

            if W == '':
                enc = lz77_encoding(x)
            else:
                enc = lz77_encoding(x, int(W))

            print("La codifica è rappresentata come:\n" + str(enc))

            dec = lz77_decoding(enc)

            print("La decodifica è: " + str(dec))

        if sel == '2':
            x = input("Inserisci il testo da codificare: ")
            print("\n")
            W = input("Inserisci la dimensione della Sliding Window (Premi Invio per Default): ")

            if W == '':
                enc = lzss_encoding(x)
            else:
                enc = lzss_encoding(x, int(W))

            print("La codifica è rappresentata come:\n" + str(enc))

            dec = lzss_decoding(enc)

            print("La decodifica è: " + str(dec))

        if sel == '3':
            x = input("Inserisci il testo da trasformare: ")

            enc = BWT(x)

            print("Il risultato della BWT è " + str(enc))

        if sel == '4':
            while True:
                print("\n\
                    1) Confronta numero di Terzine/Coppie con le Run della BWT\n\
                    2) Calcola i valori di z (Numero di Terzine) ed r (Numero di Run) per differenti Stringhe\n\
                    3) Exit")
                y = input("Seleziona: ")
                print("\n")

                if y == '1':

                    compare_triplets_runs(5,100)

                elif y == '2':
                    print("\n\
                          Insieme delle word formate come concatenazione multipla della stringa 'ab^j^k'")
                    k = input("Inserisci il valore di 'k' (max 5): ")
                    i = input("Inserisci il valore di 'i' (max 7): ")
                    if int(k) > 5:
                        k = 5
                    if int(i) > 7:
                        i = 7
                    print(str(ex_1(int(k), int(i))))
                    print("\n")

                    print("\n\
                          Insieme delle word di Fibonacci di posizione dispari fino alla i-ima")
                    i = input("Inserisci il valore di i (max 20): ")
                    if int(i) > 20:
                        i = 20
                    print(str(ex_2(int(i))))
                    print("\n")

                    print("\n\
                          Insieme delle word di Fibonacci di posizione pari fino alla i-ima")
                    i = input("Inserisci il valore di i (max 20): ")
                    if int(i) > 20:
                        i = 20
                    print(str(ex_3(int(i))))
                    print("\n")

                    print("\n\
                          Insieme delle word (s_i || e_i) || q_k, dove:\n\
                          s_i = ab^(i)aa\n\
                          e_i = ab^(i)aba^(i-2)\n\
                          q_k = ab^(k)a\n\
                          E dove s_i ed e_i sono concatenate molteplici volte per un indice i tale che:\n\
                          2 <= i <= k-1")
                    k = input("Inserisci il valore di 'k' (max 150): ")
                    if int(k) > 150:
                        k = 150
                    print(str(ex_4(int(k))))

                elif y == '3':
                    break

        if sel == '5':
            break

