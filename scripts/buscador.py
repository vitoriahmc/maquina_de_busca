import json
from argparse import ArgumentParser
from nltk.stem import PorterStemmer
from nltk.tokenize import sexpr_tokenize
from nltk.metrics.distance import edit_distance
import search_engine.repository as se

def distance_match(word, vocab):
    m = 10e5
    w = ''
    ps = PorterStemmer()
    word = ps.stem(word)
    if word in vocab:
        return word
    for word2 in vocab:
        dist = edit_distance(word, word2) 
        if dist == 0:
            w = word
            break
        if dist < m:
            m = dist
            w = word2
            
    print(f"Você quis dizer {w} ?")
    print(f"Exibindo sugestões para {w}")
    print("---------------------------------------------")
    return w

    
def busca_and(index, query, vocab):
    query_terms = query.strip().split()
    if len(query_terms) == 0:
        return {}

    initial_term = query_terms[0]
    initial_term = distance_match(initial_term, vocab)
    docids = set(index[initial_term]) if initial_term in index else set()
    words = []
    ps = PorterStemmer()
    for word in query_terms[1:]:
        word = distance_match(word, vocab)
        word = ps.stem(word)
        result = set(index[word]) if word in index else set()
        words.append(word)
        docids &= result

    return docids, words

def busca_docids(index, query, vocab):
    result = [q.strip().strip('()') for q in sexpr_tokenize(query)]

    docids = set()
    for subquery in result:
        res, words = busca_and(index, subquery, vocab)
        docids |= res

    return docids, words

def busca(corpus, repo, index, query):
    # Parsing da query.
    # Recuperar os ids de documento que contem todos os termos da query.
    vocab = []
    for k, v in repo.items():
        vocab += v
    vocab = set(vocab)
    docids, words = busca_docids(index, query, vocab)
    
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
   # print(ranked_docs[0:10])
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

    print()
    for doc in docs:
        print("-" * 100)
        print(doc)

    print(f'Numero de resultados: {len(docids)}')

if __name__ == '__main__':
    main()