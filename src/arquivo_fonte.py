import re

from src.reconhecedor.tabela.simbolo import Simbolo

SEPARADOR = ' '
OPERADORES = ('+', '-', '*', '/', '(', ')', '[', ']', '{', '}', '>=', '<=', '==', '<', '>', ',', ';')


def ler_fonte(path: str):
    """
    Lê o arquivo-fonte e retorna a lista de todos os seus tokens
    :param string path: caminho para o arquivo-fonte
    :return list<objects>:
    """

    tokens = []
    try:
        with open(path, encoding='utf-8') as arquivo:
            num_linha = 1
            for linha in arquivo:

                linha = remover_quebra_de_linhas(linha)
                linha = espaca_operadores(linha)

                for token in pegar_tokens(linha):
                    tokens.append(Simbolo(token, num_linha))

                num_linha += 1

    except Exception as e:
        print('Erro ao ler arquivo de fonte. ' + str(e))
        exit()

    return tokens


def remover_quebra_de_linhas(linha):
    """
    Remove as quebras de linha de um texto
    :param string linha:
    :return string:
    """
    return linha.replace('\n', '').replace('\r', '')


def pegar_tokens(linha):
    """
    Retorna os tokens de uma linha
    :param string linha:
    :return string:
    """
    return [token for token in linha.split(SEPARADOR) if token != '']


def espaca_operadores(linha):
    """
    Retorna a linha com espaçamento nos separadores
    :param string linha:
    :return string:
    """
    regex = f'({"|".join(re.escape(op) for op in OPERADORES)})'
    linha = re.sub(regex, r' \1 ', linha)
    return linha


if __name__ == '__main__':
    print(ler_fonte('../arquivos/fonte.txt'))
