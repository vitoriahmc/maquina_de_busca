import json
from argparse import ArgumentParser


def busca(index, repo, query):
    # Parsing da query.

    # Recuperar os ids de documento que contem todos os termos da query.

    # Retornar os textos destes documentos.
    pass


def main():
    parser = ArgumentParser()
    parser.add_argument('repo', help='Arquivo do repo.')
    parser.add_argument('index', help='Arquivo do index.')
    parser.add_argument('query', help='A query (entre aspas)')
    args = parser.parse_args()

    with open(args.repo, 'r') as file:
        repo = json.load(file)

    with open(args.index, 'r') as file:
        index = json.load(file)


if __name__ == '__main__':
    main()
