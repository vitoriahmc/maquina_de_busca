import json
from argparse import ArgumentParser
from nltk.stem import PorterStemmer
from nltk.tokenize import sexpr_tokenize
from nltk.metrics.distance import edit_distance
import search_engine.repository as se

def distance_match(word, vocab):
    m = 10e5
    w = ''
    for word2 in vocab:
        dist = edit_distance(word, word2) 
        if dist == 0:
            w = word
            break
        if dist < m:
            m = dist
            w = word2
    return f"Você quis dizer {w} ?"

    
def busca_and(index, query):
    query_terms = query.strip().split()
    if len(query_terms) == 0:
        return {}

    initial_term = query_terms[0]
    docids = set(index[initial_term]) if initial_term in index else set()
    words = []
    ps = PorterStemmer()
    for word in query_terms[1:]:
        word = ps.stem(word)
        result = set(index[word]) if word in index else set()
        words.append(word)
        docids &= result

    return docids, words

def busca_docids(index, query):
    result = [q.strip().strip('()') for q in sexpr_tokenize(query)]

    docids = set()
    for subquery in result:
        res, words = busca_and(index, subquery)
        docids |= res

    return docids, words

def busca(corpus, repo, index, query):
    # Parsing da query.
    # Recuperar os ids de documento que contem todos os termos da query.
    docids, words = busca_docids(index, query)
    
    # Retornar os textos destes documentos.
    return docids, words


def ranking(ranking_doc, docids, words):
    ranked_docs = []
    for doc_id in docids:
        total = 0
        for word in words:
            tf = ranking_doc[doc_id][word]
            idf = ranking_doc['idf'][word]
            total += tf * idf
        ranked_docs.append([doc_id, total])

    ranked_docs = sorted(ranked_docs, key= lambda x: x[1])
    return [doc_id for doc_id, _ in ranked_docs]

def main():
    parser = ArgumentParser()
    parser.add_argument('corpus', help='Arquivo do corpus')
    parser.add_argument('repo', help='Arquivo do repo.')
    parser.add_argument('index', help='Arquivo do index.')
    parser.add_argument('ranking_file', help='Arquivo do index.')
    parser.add_argument('num_docs',
                        help='Numero maximo de documentos a retornar',
                        type=int)
    parser.add_argument('query', help='A query (entre aspas)')
    args = parser.parse_args()

    corpus = se.load_corpus(args.corpus)

    with open(args.repo, 'r') as file:
        repo = json.load(file)

    with open(args.index, 'r') as file:
        index = json.load(file)
    
    with open(args.ranking_file, 'r') as file:
        ranking_doc = json.load(file)

    docids, words = busca(corpus, repo, index, args.query)
    docids_ranqueados = ranking(ranking_doc, docids, words)
    docs = [corpus[docid] for docid in docids_ranqueados[:args.num_docs]]

    print(docs)

    print(f'Numero de resultados: {len(docids)}')

if __name__ == '__main__':
    main()