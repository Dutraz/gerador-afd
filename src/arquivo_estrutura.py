import filecmp
import os
import re
import shutil


def verifica_alteracao(path):
    # Se o arquivo de estruturas em cache já existe e foi alterado
    alterou = not (
            os.path.isfile('arquivos/cache/estruturas.txt') and filecmp.cmp(path, 'arquivos/cache/estruturas.txt')
    )

    # Agora que já verificou alteração, copia o arquivo para a cache
    shutil.copyfile(path, 'arquivos/cache/estruturas.txt')

    return alterou


def ler_estruturas(path: str):
    gramatica = {}

    with open(path, encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.split('//')[0]
            if linha.strip():
                nao_terminal, producoes = linha.strip().split('::=')
                nao_terminal = nao_terminal.strip().replace('<', '').replace('>', '')
                producoes = [
                    remove_multiplos_espacos(p.replace('<', ' ').replace('>', ' ').replace('ε', '\'\'').strip())
                    for p in producoes.split('|')
                ]
                gramatica[nao_terminal] = producoes

    gramatica_formatada = 'S\' -> S\n'
    for nao_terminal, producoes in gramatica.items():
        for producao in producoes:
            gramatica_formatada += f"{nao_terminal} -> {producao} \n"

    return gramatica_formatada


def remove_multiplos_espacos(string):
    return re.sub(r'\s+', ' ', string)


if __name__ == '__main__':
    print(ler_estruturas('../arquivos/estruturas.txt'))
