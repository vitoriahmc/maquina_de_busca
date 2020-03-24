import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from argparse import ArgumentParser
from collections import defaultdict

def create_repo(corpus):
    '''Cria o repositorio.

    Args:
        corpus: dicionario que mapeia um docid para uma string contendo o
                documento completo.

    Returns:
        Um dicionário que mapeia docid para uma lista de tokens.
    '''
    repo = {}
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    for docid, string in corpus.items():
        tokens = nltk.word_tokenize(string)
        stemmed = [ps.stem(x) for x in tokens if not x in stop_words] 
        clean = [w for w in stemmed if w.isalpha()]
        repo[docid] = clean
    return repo


def create_index(repo):
    '''Indexa os documentos de um corpus.

    Args:
        repo: dicionario que mapeia docid para uma lista de tokens.

    Returns:
        O índice reverso do repositorio: um dicionario que mapeia token para
        lista de docids.
    '''
    indexed = defaultdict(set)

    for k,v in repo.items():
        for word in v:
            indexed[word].add(k)

    for key in indexed:
        indexed[key] = list(indexed[key])
    return indexed

def main():
    parser = ArgumentParser()
    parser.add_argument('corpus',
                        help='Arquivo json com um dicionario docid para texto')
    parser.add_argument('repo_name',
                        help='Raiz do nome do arquivo de repositorio')
    args = parser.parse_args()

    with open(args.corpus, 'r') as file_corpus:
        corpus = json.load(file_corpus)

    repo = create_repo(corpus)
    index = create_index(repo)

    with open(args.repo_name + '_repo.json', 'w') as file_repo:
        json.dump(repo, file_repo, indent=4)

    with open(args.repo_name + '_index.json', 'w') as file_index:
        json.dump(index, file_index, indent=4)

if __name__ == '__main__':
    main()
