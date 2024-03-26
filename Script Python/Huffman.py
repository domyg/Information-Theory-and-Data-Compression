############
## IMPLEMENTAZIONE ALGORITMO DI CODIFICA DI HUFFMAN ##
############


"""
Dato un testo T dovrò:

1) Contare le occorrenze di ogni simbolo 'a' in T e calcolare, per questo simbolo,
la probabilità corrispondente.

2) Inserire nella Coda con Priorità ogni simbolo con la sua probabilità corrispondente

3) Estrarre dalla Coda i due Nodi con probabilità più bassa e formare, a partire da questi, un nodo
genitore avente come probabilità la somma delle probabilità dei suddetti nodi.

4) Aggiungere il nuovo nodo genitore alla Coda

Considerando l'Algoritmo per la Codifica di Huffman, a ogni nodo sinistro concatenerò uno 0 nella codeword
di quel percorso; analogamente, per ogni nodo destro, concatenerò un 1
"""

from queue import PriorityQueue

# Creo la Classe Nodo per definire gli oggetti attraverso cui si potrà costruire un Albero.
class Node(object):
    def __init__(self, symbol, prob, left=None, right=None):
        self.left = left
        self.right = right
        self.symbol = symbol
        self.prob = prob

        self.codeword = ""

    def __eq__(self, other):
        return (self.prob == other.prob) and (self.symbol == other.symbol)

    def __ne__(self, other):
        return not (self == other)

    def has_children(self):
        if self.left or self.right:
            return True
        else:
            return False
    
    def __str__(self) -> str:
        print("\nNodo:" + self.symbol)
        if self.left:
            print("Figlio Sinistro: " + self.left.symbol)
        if self.right:
            print("Figlio Destro: " + self.right.symbol)
        
        return ""


    # La funzionalità di confronto Less Than è stata implementata in modo tale che, qualore le
    # probabilità di due simboli fossero le stesse, verrebbe considerato come simbolo più piccolo
    # quello alfabeticamente minore
    def __lt__(self, other):
        if self.prob == other.prob:
            return ord(self.symbol[0]) < ord(other.symbol[0])
        else:
            return (self.prob < other.prob)
    

# La seguente funzione calcola la probabilità associata a ogni simbolo del testo
def prob_calc(text):
    char_freq = {}
    length = len(text)

    # Con questo ciclo iterativo calcolo le occorrenze di ogni carattere all'interno del testo
    for c in text:
        if c in char_freq:
            char_freq[c] +=1
        else:
            char_freq[c] = 1

    # Definisco un Dizionario composto da coppie (Character - Probability) per calcolare la
    # probabilità associata a ogni carattere
    char_prob = {}
    for c in char_freq:
        char_prob[c] = char_freq[c]/length

    return char_prob

# Funzione utilizzata per creare una Coda con Priorità che contiene tutti gli elementi del
# Dizionario Char_Prob
def create_queue(char_prob: dict):
    prio_queue = PriorityQueue()
    for c in char_prob.keys():
        prio_queue.put(Node(c, char_prob[c]))
    return prio_queue


# Funzione utilizzata per la creazione dei Nodi dell'Albero di Huffman utilizzato per creare il Codice
def create_nodes(prio_queue: PriorityQueue) -> Node:

    # Itero fino a quando nella coda non rimane un unico Nodo, ovvero il Nodo radice
    while(prio_queue.qsize() > 1):

        left = prio_queue.get()
        right = prio_queue.get()

        # Ogni volta che creo estraggo un elemento dalla coda creo un nodo e associo a esso un
        # frammento di codeword.
        # In particolare, se è un Nodo sinistro associo '0', altrimenti associo '1'
        left.codeword = '0'
        right.codeword = '1'

        # Dai due nodi estratti dalla coda ne compongo uno nuovo e lo reinserisco in coda
        new_node = Node(left.symbol + right.symbol, left.prob + right.prob, left, right)
        prio_queue.put(new_node)

    # Terminate le iterazioni restituisco il Nodo Radice
    return prio_queue.get()


# Funzione che crea il codice associato a ogni Simbolo
def make_codes(node: Node, code="", codes = {}) -> dict:

    # Dato il valore della codeword del nodo corrente, vado componendo la codeword risultante 
    # da ogni discesa lungo l'albero fino al raggiungimento di un nodo foglia.
    # Sfrutto il concetto di ricorsione per mantenere aggiornato il valore della variabile 'value'
    # e utilizzarlo alla fine di ogni chiamata alla funzione per memorizzarlo in corrispondenza del
    # Simbolo del nodo foglia raggiunto.
    value = code + node.codeword

    if(node.left):
        make_codes(node.left, value)

    if(node.right):
        make_codes(node.right, value)

    if(not node.left and not node.right):
        codes[node.symbol] = value
    
    return codes


# Funzione che crea il Codice di Huffman per i Simboli contenuti nel testo fornito come parametro
def create_huffman(text: str):
    
    # Calcolo le probabilità associate a ogni simbolo
    char_prob = prob_calc(text)

    # Creo una Coda con Priorità che contiene i Simboli e li estrae secondo il loro valore minimo di priorità
    queue = create_queue(char_prob)

    # Crea l'oggetto Radice dell'Albero che rappresenta l'intero Albero di Huffman
    tree_root = create_nodes(queue)

    # Genero tutti i Codici a partire dall'Albero di Huffman
    code = make_codes(tree_root)

    # Restituisco la coppia 'Codice' - 'Albero' al fine di poter passare questo al Decoder
    return code, tree_root


# Funzione che effettua la Codifica di Huffman del Testo fornito come parametro (Sfrutta la funzione precedente)
def huffman_encoding(text) -> str:
    
    code, tree_root = create_huffman(text)

    output = []

    # Itero lungo i caratteri del testo di input e vado costruendo la lista composta dai caratteri
    # codificati ottenuti dal Codice di Huffman
    for symbol in text:
        output.append(code[symbol])

    # Genero la Stringa di output
    encoded_string = ''.join([str(item) for item in output])

    return encoded_string, tree_root


# Funzione che, a partire da un testo Codificato e dall'Albero di Huffman corrispondente, decodifica un messaggio
def huffman_decoding(encoded_text, tree_root: Node) -> str:
    
    output = []

    # Memorizzo l'Albero originale in una variabile che utilizzerò per ricominciare dal Nodo Radice
    # una volta raggiunto un Nodo Foglia
    temp_root = tree_root

    # Per ogni carattere del testo codificato verifico se spostarmi sul sottoalbero sinistro (0) o destro (1)
    for x in encoded_text:  
        if x == '1':
            tree_root = tree_root.right   

        elif x == '0':  
            tree_root = tree_root.left   

        if (tree_root.left or tree_root.right):  
            continue

        # Al raggiungimento di un Nodo Foglia ne estraggo il Simbolo corrispondente e lo appendo alla lista
        # che rappresenta l'output
        else:
            output.append(tree_root.symbol)  

            # Reinizializzo il valore del Nodo corrente con quello del Nodo Radice originale,
            # potendo così ripercorrere l'Albero
            tree_root = temp_root 

    # Costruisco la Stringa Decodificata a partire dalla Lista 'output'      
    string = ''.join([str(item) for item in output]) 
    return string  


def huffman():

        
    text = input("Inserisci il Testo di cui effettuare la Codifica di Huffman \n")

    code = create_huffman(text)[0]
    encoded_text, tree_root = huffman_encoding(text)

    print("Il Codice di Huffman generato è il seguente: \n")
    print(code)
    print("\n \nIl testo \n'" + text + "'\nviene codificato nel testo seguente: \n")
    print(encoded_text)
    decoded_text = huffman_decoding(encoded_text, tree_root)
    print("\n \nLa Decodifica del testo codificato\n'" + encoded_text + "'\nviene decifrata nel testo seguente:\n")
    print(decoded_text)
