import json
from argparse import ArgumentParser
from nltk.stem import PorterStemmer

def busca(index, data, query):
    # Parsing da query.

    # Recuperar os ids de documento que contem todos os termos da query.

    # Retornar os textos destes documentos.

    words = query.split(' ')
    ps = PorterStemmer()
    sets = set(index[ps.stem(words[0])])
    for i in range(1, len(words)):
        word_stemmed = ps.stem(words[i])
        s = set(index[word_stemmed])
        sets = sets.intersection(s)

    print([data[doc_id] for doc_id in sets])

    return [data[doc_id] for doc_id in sets]

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