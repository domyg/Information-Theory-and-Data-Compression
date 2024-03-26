############
## IMPLEMENTAZIONE ALGORITMI DI CODIFICA UNIVERSALE PER INTERI ##
############


import math
import matplotlib.pyplot as plt
import numpy as np
import random

def gamma_encoding(x: str) -> str:

    # Creo una lista che memorizzerà i singoli bit rappresentanti l'output
    output = []

    # Calcolo il valore dell'esponente della più grande potenza di 2 minore del numero x da codificare.
    # Questo valore corrisponde a |B(x)| - 1, ovvero la quantità di zeri che precederà la rappresentazione
    # binaria del numero da codificare.
    N = math.floor(math.log2(int(x)))

    # Scrivo N volte il bit '0' all'interno della stringa di output.
    for i in range(N):
        output.append('0')
    
    # Concateno alla suddetta stringa la rappresentazione binaria del numero x da codificare.
    output.append(bin(int(x))[2:])

    # Costurisco la Stringa di output
    return ''.join([str(item) for item in output])


def gamma_decoding(bin: str) -> int:

    # Creo un contatore per contare il numero di '0' prima del primo '1'
    zero_counter = 0

    # Conto il numero di '0'
    for c in bin:
        if c == '0':
            zero_counter +=1
        else:
            break
    
    # Sia N il numero di bit pari a '0', la decodifica sarà ottenuta convertendo in intero la rappresentazione
    # binaria del numero binario avente come MSB quello di posizione N+1-esima.
    # N.B. uso il valore di 'zero_counter' in quanto il contatore considera '1' come prima occorrenza,
    # mentre le liste contano a partire da '0'.
    # Quindi, se ho zero bit a '0', posso cominciare a partire dalla 0-esima posizione della lista (Stringa).
    int_rep = int(bin[zero_counter:], base=2)

    return int_rep


def delta_encoding(x: str) -> str:

    output = []

    # Il valore N viene calcolato come per la Codifica Gamma
    N = math.floor(math.log2(int(x)))
    
    # Inserisco nella prima parte dell'output la Codifica Gamma del valore 'N+1'
    output.append(gamma_encoding(N+1))

    # Inserisco, infine, la rappresentazione Binaria del numero da codificare privato del suo MSB
    output.append(bin(int(x))[3:])

    return ''.join([str(item) for item in output])


def delta_decoding(bin: str) -> int:

    # Creo un contatore per i bit '0' che precedono il primo bit '1'
    zero_counter = 0

    for b in bin:
        if b == '0':
            zero_counter +=1
        else:
            break
    
    # Estraggo i primi 'zero_counter' bit dalla stringa da decodificare; Ovvero, tutti i bit '0' iniziali
    new_bin = bin[zero_counter:]

    # Estraggo dalla stringa binaria i primi 'zero_counter + 1' bit che rappresentano il valore 'N+1' di cui
    # si è calcolato il Gamma Code durante la fase di Codifica
    final_bin = new_bin[zero_counter+1:]


    # Ritorno la concatenazione tra il bit '1' e la stringa ottenuta dalle precedenti trasformazioni
    return int('1' + final_bin, base=2)


# La codifica di fibonacci nasce dall'enunciato del Teorema di Zeckendorf che dimostra come un qualunque
# numero intero positivo possa essere rappresentato come la somma di due o più numeri di Fibonacci
# in modo tale che gli addendi della somma non presentino due numeri di Fibonacci consecutivi.

# Per la Codifica di Fibonacci necessitiamo di una Funzione che calcoli la sequenza di Fibonacci fino a un
# certo valore 'x'
def get_fib_sequence(x):

    i = 1
    # Imposto i primi due valori della sequenza di Fibonacci con i valori '0' e '1'
    fib_list = [0, 1]
    
    # La lista va creata fintantoché non si ottiene un Numero di Fibonacci che risulta essere il maggiore
    # numero minore o uguale al valore 'x' da codificare
    while fib_list[i] + fib_list[i - 1] <= x:
        fib_list.append(fib_list[i] + fib_list[i - 1])
        i = i + 1
    
    # Ritorno la sola parte della lista di Fibonacci utilizzata nella rappresentazione di Zeckendorf
    return fib_list[2:]


def get_fibonacci(i):
    
    a = 0
    b = 1
    list = []
    list.append(a)

    for x in range(i):
        a, b = b, a + b
        list.append(a)
    
    return list


def fibonacci_encoding(x):

    # Genero la sequenza di Fibonacci avente come upper bound il valore 'x' e creo una lista con un numero
    # di bit '0' pari alla dimensione della suddetta sequenza.
    fib_sequence = get_fib_sequence(x)
    encoding = ['0'] * len(fib_sequence)
    
    # Itero fino a quando il resto della differenza tra il valore 'x' corrente e il massimo valore
    # della sequenza di Fibonacci attuale non risulti uguale a 0.
    while x > 0:
        # Genero la sequenza di Fibonacci per ogni nuovo valore di 'x'
        # La seguente assegnazione corrisponderebbe a una chiamata a 'get_fib_sequence(x)'
        fib_sequence = [item for item in fib_sequence if item <= x]

        # Estraggo dalla suddetta sequenza il massimo valore generato
        largest_fib = max(fib_sequence)
        # Calcolo il resto della differenza tra il valore di 'x' e il max valore della sequenza corrente
        x = x - largest_fib

        # Calcolo l'indice del massimo numero di Fibonacci considerando la rappresentazione di Zeckendorf
        i  = fib_sequence.index(largest_fib)

        # Inserisco il bit '1' all'i-esima posizione (i-2 nell'Algoritmo che considera l'intera sequenza Fib)
        encoding[i] = '1' 
            
    # Inserisco il bit '1' come suffisso
    encoding.append('1')
        
    return "".join(encoding)


def fibonacci_decoding(bin):

    # Rimuovo il LSB dalla sequenza da Decodificare
    bin = bin[:-1]
    output = 0

    # Creo un indice con valore '2' per cominciare dal Terzo numero della Sequenza di Fibonacci
    # che corrisponde al primo numero considerato nella rappresentazione di Zeckendorf
    pos = 2

    # Ricavo la lista dei primi N numeri di Fibonacci, considerando N come la lunghezza della sequenza
    # binaria da decodificare
    fibonacci_sequence = get_fibonacci(len(bin)+1)

    # Scansiono i bit della sequenza da decodificare, considerandone la posizione, sommando tra loro
    # tutti i numeri di Fibonacci aventi posizione corrispondente alla posizione dei bit con valore '1'
    for b in bin:        
        if b == '1':
            output = output + fibonacci_sequence[pos]
        pos = pos + 1
    
    return str(output)


def levenshtein_encoding(x):
    
    # La codifica di Levenshtein di '0' è sempre '0'
    if x == '0':
        return '0'
    
    count = 0
    output = ''

    while x != 0:
        # Scrivo la rappresentazione Binaria eliminando la prima parte che identifica la base ('0b') e il MSB
        binary_str = str(bin(int(x)))[3:]
        count += 1

        # Aggiungo come prefisso della Stringa di output corrente la rappresentazione binaria del numero
        # corrente privata del suo MSB
        output = binary_str + output

        # Calcolo il numero di bit che compongono la suddetta rappresentazione
        x = len(binary_str)

    # Creo una stringa per memorizzare il prefisso dell'intero output che sarà composto da un numero di bit
    # posti a '1' pari a ' count ' seguiti da un bit posto a '0'
    prefix = ''
    for i in range(count):
        prefix += '1'

    prefix += '0'

    # Ritorno la stringa di output come contatenazione tra il Prefisso e l'Output calcolato in precedenza
    return prefix + output


def levenshtein_decoding(bin):
    
    count = 0

    # Sfrutto la variabile 'count' per contare il numero di bit '1' che precedono il primo bit '0'
    for c in bin:
        if c == '0':
            break
        count += 1

    if count == 0:
        return '0'
    
    # Considero la sola parte di rappresentazione binaria che segue dopo il primo bit '0' incontrato
    bin = bin[count+1:]

    N = 1

    # Itero 'count-1' volte
    for i in range(count-1):

        # Estraggo i primi N bit dalla stringa corrente
        bits = bin[:N]

        # Aggiorno la stringa corrente eliminando i bit appena letti
        bin = bin[N:]

        # Antepongo ai bit letti il bit '1'
        bits = '1' + bits

        # Calcolo il valore intero che i bit estratti, concatenati al bit '1', rappresentano
        N = int(bits, base=2)

    # Ritorno la stringa Decodificata
    return str(N)


def rice_code_encoding(x, k):
    
    # Calcolo il quoziente come parte intera inferiore del rapporto tra il numero che precede 'x' e la
    # k-esima potenza di 2
    q = math.floor((int(x)-1)/pow(2,int(k)))

    # Calcolo il resto come differenza tra il numero da Codificare 'x' e il valore '(2^k * q - 1)'
    r = int(x) - pow(2,int(k))*q - 1

    # Scrivo la prima parte della codeword come stringa unaria di 'q'
    unary_prefix = '0'*q + '1'

    # Concateno la rappresentazione binaria del valore di 'r' codificata con esattamente 'k' bits.
    suffix = bin(r)[2:].zfill(int(k))

    return unary_prefix + suffix


def rice_code_decoding(bin, k):

    q = 0

    # Calcolo il valore di quoziente sommando il numero di bit a '0' che precedono il primo bit a '1'
    for b in bin:
        if b == '1':
            break
        q += 1

    # Calcolo il valore del Resto convertendo in Intero la sua rappresentazione Binaria situata dopo la stringa
    # unaria che rappresenta il quoziente
    r = int(bin[q+1:], base=2)

    # Sfrutto la formula per il calcolo del Resto per risalire al valore del numero originale 'x'
    return r + pow(2,k)*q + 1


def plot_len_stats(upper_bound):
    x_axis = np.arange(upper_bound)
    gamma_axis = np.zeros(upper_bound)
    delta_axis = np.zeros(upper_bound)
    fibonacci_axis = np.zeros(upper_bound)
    lev_axis = np.zeros(upper_bound)
    rice_5_axis = np.zeros(upper_bound)
    rice_7_axis = np.zeros(upper_bound)

    for n in range(1, upper_bound):
        gamma_axis[n] = len(gamma_encoding(n))
        delta_axis[n] = len(delta_encoding(n))
        fibonacci_axis[n] = len(fibonacci_encoding(n))
        lev_axis[n] = len(levenshtein_encoding(n))
        rice_5_axis[n] = len(rice_code_encoding(n,5))
        rice_7_axis[n] = len(rice_code_encoding(n,7))


    plt.plot(x_axis, gamma_axis, c='blue', label="Gamma")
    plt.plot(x_axis, delta_axis, c='green', label="Delta")
    plt.plot(x_axis, fibonacci_axis, c='red', label="Fibonacci")
    plt.plot(x_axis, lev_axis, c='orange', label="Levensthein")
    plt.plot(x_axis, rice_5_axis, c='purple', label="Rice_5")
    plt.plot(x_axis, rice_7_axis, c='brown', label="Rice_7")
    plt.legend()
    plt.ylabel('N° Bits')
    plt.xlabel('Numero Intero')
    plt.title('Encoding Length per Algoritmo')

    plt.show()


# La seguente funzione svolge 3 differenti esperimenti che calcolano la quantità di bits necessaria a
# codificare dei valori interi scelti in modi differenti
def compute_lengths():

    print("1) Bits richiesti per 100 Interi nel range [1-100000]\n\
2) Bits richiesti per 100 Interi nel range [1-1000] estratti in modo Casuale\n\
3) Bits richiesti per 1000 Interi estratti da una Distribuzione Normale Nota\n")
    experiment = input("Seleziona quale esperimento avviare: ")

    n = 100
    length = [0,0,0,0,0,0,0]
    mean = [0,0,0,0,0,0,0]
    algorithms = ['Gamma', 'Delta', 'Fib', 'Leven', 'Rice_5', 'Rice_7', 'Binary']
    upper_bound = 0

    if experiment == '1':
        
        print("Esperimento 1) \n\n")
        for i in range(1, 100000, 1010):
            length[0] += len(gamma_encoding(i))
            length[1] += len(delta_encoding(i))
            length[2] += len(fibonacci_encoding(i))
            length[3] += len(levenshtein_encoding(i))
            length[4] += len(rice_code_encoding(i, 5))
            length[5] += len(rice_code_encoding(i, 7))
            length[6] += len(bin(i)[2:])
            upper_bound += 1

        for i in range(len(mean)):
            mean[i] = length[i]/n
        
        for i in range(len(mean)):
            print(str(algorithms[i]) + '\tMean: ' + str(mean[i]) + '\t\tNumber of Bits: ' + str(length[i])
                 + '\n')

    elif experiment == '2':

        upper_bound = 100
        print("Esperimento 2) \n\n")
        for x in range(0,upper_bound):
            i = random.randint(1,1000)
            length[0] += len(gamma_encoding(i))
            length[1] += len(delta_encoding(i))
            length[2] += len(fibonacci_encoding(i))
            length[3] += len(levenshtein_encoding(i))
            length[4] += len(rice_code_encoding(i, 5))
            length[5] += len(rice_code_encoding(i, 7))
            length[6] += len(bin(i)[2:])

        for i in range(len(mean)):
            mean[i] = length[i]/n
        
        for i in range(len(mean)):
            print(str(algorithms[i]) + '\tMean: ' + str(mean[i]) + '\t\tNumber of Bits: ' + str(length[i]) + '\n')

    
    elif experiment == '3':

        upper_bound = 1000
        print("Seleziona i parametri della Distribuzione Normale\n")
        mean_input = float(input("Seleziona la Media: "))
        dev = float(input("Seleziona la Devianza: "))
        numbers = []

        for i in range(upper_bound):

            numbers.append(math.ceil(np.random.normal(mean_input, dev)))

        for n in numbers:

            # Modifico i numeri che non possono essere utilizzati per la codifica (Negativi o uguali a 0)
            if n < 0:
                n = -n
            elif n == 0:
                n = n + 1              
            length[0] += len(gamma_encoding(n))
            length[1] += len(delta_encoding(n))
            length[2] += len(fibonacci_encoding(n))
            length[3] += len(levenshtein_encoding(n))
            length[4] += len(rice_code_encoding(n, 5))
            length[5] += len(rice_code_encoding(n, 7))
            length[6] += len(bin(n)[2:])

        for i in range(len(mean)):
            mean[i] = length[i]/upper_bound

        for i in range(len(mean)):
            print(str(algorithms[i]) + '\t Mean:' + str(mean[i]) + '\t\tNumber of Bits: ' + str(length[i]) + '\n')

    n_bars = np.arange(7)

    plt.bar(n_bars, length, align='center')
    plt.xticks(n_bars, algorithms)
    plt.ylabel('N° Bits')
    plt.xlabel('Algoritmo')
    plt.title('Bits per Algoritmo')
    plt.show()

    return True


# Menù interattivo per interagire con il programma
def integer_coding_menu():

    print("Benvenut* nel Menù di Codifica Universale per gli Interi!\n")

    while True:
        print("\n\
            1) Gamma Encoding\n\
            2) Delta Encoding\n\
            3) Fibonacci Encoding\n\
            4) Levenshtein Encoding\n\
            5) Rice Encoding\n\
            6) Esperimenti\n\
            7) Exit\n")
        
        sel = input("Seleziona cosa fare: ")

        if sel == '1':
            x = input("Inserisci il numero da codificare: ")

            enc = gamma_encoding(x)
            print("La codifica del numero scelto è: " + enc)

            dec = gamma_decoding(enc)

            print("La decodifica è: " + str(dec))

        if sel == '2':
            x = input("Inserisci il numero da codificare: ")

            enc = delta_encoding(x)
            print("La codifica del numero scelto è: " + enc)

            dec = delta_decoding(enc)

            print("La decodifica è: " + str(dec))

        if sel == '3':
            x = int(input("Inserisci il numero da codificare: "))

            enc = fibonacci_encoding(x)
            print("La codifica del numero scelto è: " + enc)

            dec = fibonacci_decoding(enc)

            print("La decodifica è: " + str(dec))

        if sel == '4':
            x = int(input("Inserisci il numero da codificare: "))

            enc = levenshtein_encoding(x)
            print("La codifica del numero scelto è: " + enc)

            dec = levenshtein_decoding(enc)

            print("La decodifica è: " + str(dec))

        if sel == '5':
            x = int(input("Inserisci il numero da codificare: "))
            k = int(input("Inserisci il valore di K per la Rice Encoding: "))

            enc = rice_code_encoding(x, k)
            print("La codifica del numero scelto è: " + enc)

            dec = rice_code_decoding(enc, k)

            print("La decodifica è: " + str(dec))

        if sel == '6':
            compute_lengths()
            plot_len_stats(1001)

        if sel == '7':
            break