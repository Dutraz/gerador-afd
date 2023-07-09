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
    gramatica = [{
        'simbolo': 'S\'',
        'producao': 'S',
        'tamanho': 1,
        'acoes': None,
    }]

    with open(path, encoding='utf-8') as arquivo:
        for linha in arquivo:

            # Remove os comentários
            linha = linha.split('//')[0]

            if linha.strip():
                # Separa o símbolo das produções e ações
                nao_terminal, producao_acao = linha.strip().split('::=')

                nao_terminal = nao_terminal.strip().replace('<', '').replace('>', '')

                # Separa as produções das ações
                producao_acao = producao_acao.strip().split('{{')

                producao = remove_multiplos_espacos(
                    producao_acao[0].replace('<', ' ').replace('>', ' ').replace('ε', '\'\'').strip()
                )

                acoes = None

                if len(producao_acao) > 1:
                    acoes = producao_acao[1].replace('}}', '').strip().split(';')

                gramatica.append({
                    'simbolo': nao_terminal,
                    'producao': producao,
                    'tamanho': len(producao.split()),
                    'acoes': acoes,
                })

    return gramatica


def remove_multiplos_espacos(string):
    return re.sub(r'\s+', ' ', string)


if __name__ == '__main__':
    print(ler_estruturas('../arquivos/estruturas.txt'))
