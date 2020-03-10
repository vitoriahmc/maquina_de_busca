import json
from argparse import ArgumentParser


def create_repo(corpus):
    '''Cria o repositorio.

    Args:
        corpus: dicionario que mapeia um docid para uma string contendo o
                documento completo.

    Returns:
        Um dicionário que mapeia docid para uma lista de tokens.
    '''
    return {}


def create_index(repo):
    '''Indexa os documentos de um corpus.

    Args:
        repo: dicionario que mapeia docid para uma lista de tokens.

    Returns:
        O índice reverso do repositorio: um dicionario que mapeia token para
        lista de docids.
    '''
    return {}


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
        json.dump(repo, file_repo)

    with open(args.repo_name + '_index.json', 'w') as file_index:
        json.dump(repo, file_index)


if __name__ == '__main__':
    main()
