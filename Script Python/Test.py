import SardinasPatterson as SP
import Huffman
import IntegerEncoding as IE
import LZEncoding as LZ
import StringAttractor as SA
import REPAIR

while True:
    print("Seleziona la categoria da visitare\n\
        1) Sardinas-Patterson\n\
        2) Huffman Encoding\n\
        3) Integer Encoding\n\
        4) LZ Encoding\n\
        5) String Attractor\n\
        6) RE-PAIR\n\
        7) Exit")
    x = input()


    if x == '1':

        SP.sardinas_patterson()

    elif x == '2':

        Huffman.huffman()

    elif x == '3':
    
        IE.integer_coding_menu()

    elif x == '4':

        LZ.lz_coding_menu()

    elif x == '5':
        SA.string_attractor_menu()

    elif x == '6':
        REPAIR.repair_menu()

    elif x == '7':
        break