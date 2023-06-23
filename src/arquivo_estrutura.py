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

            # Remove os cometários
            linha = linha.split('//')[0]

            if linha.strip():
                # Separa o símbolo das produções
                nao_terminal, producao = linha.strip().split('::=')

                nao_terminal = nao_terminal.strip().replace('<', '').replace('>', '')
                producao = remove_multiplos_espacos(
                    producao.replace('<', ' ').replace('>', ' ').replace('ε', '\'\'').strip()
                )

                if nao_terminal not in gramatica:
                    gramatica[nao_terminal] = []

                gramatica[nao_terminal].append(
                    producao
                )

    gramatica_cfg = [{
        'simbolo': 'S\'',
        'producao': 'S',
        'tamanho': 1,
    }]
    for nao_terminal, producao in gramatica.items():
        for p in producao:
            gramatica_cfg.append({
                'simbolo': nao_terminal,
                'producao': p,
                'tamanho': len(p.split())
            })

    return gramatica_cfg


def remove_multiplos_espacos(string):
    return re.sub(r'\s+', ' ', string)


if __name__ == '__main__':
    print(ler_estruturas('../arquivos/estruturas.txt'))
