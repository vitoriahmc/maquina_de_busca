import json
from argparse import ArgumentParser
from nltk.stem import PorterStemmer
from nltk.tokenize import SExprTokenizer

def busca(index, data, query):
    # Parsing da query.

    # Recuperar os ids de documento que contem todos os termos da query.

    # Retornar os textos destes documentos.

    ps = PorterStemmer()
    words = []
    def parse(exp):
        print(exp)
        sets = ()
        tokenized = SExprTokenizer().tokenize(exp)
        for token in tokenized:
            if '(' in token:
                words.append("(")
                s = parse(token[1:-1])
                words.append(")")
            else:
                word = token.split(" ")
                for w in word:
                    words.append(w)   
            print('token:', token)
        print(words)

                
        
    sets = set()
    #query = '(a b (c d)) e f (g)'
    parse(query)
    print(sets)
    # print([data[doc_id] for doc_id in sets])

    # return [data[doc_id] for doc_id in sets]

def main():
    parser = ArgumentParser()
    parser.add_argument('data', help='Arquivo com dados brutos.')
    parser.add_argument('index', help='Arquivo do index.')
    parser.add_argument('query', help='A query (entre aspas)')
    args = parser.parse_args()

    with open(args.data, 'r') as file:
        data = json.load(file)

    with open(args.index, 'r') as file:
        index = json.load(file)
    
    busca(index, data, args.query)

if __name__ == '__main__':
    main()