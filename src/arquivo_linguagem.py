import re

from src.linguagem.gramatica.gramatica import Gramatica
from src.linguagem.gramatica.regra import Regra
from src.linguagem.gramatica.simbolo import SimboloNaoTerminal, SimboloTerminal, Epsilon
from src.util import gerador_de_tokens


def ler_linguagem(path: str):
    gramaticas = []

    try:
        with open(path, encoding='utf-8') as arquivo:

            # Flag indicando se esta no meio da leitura de uma gramática
            gramatica = Gramatica()
            modo_gramatica = False

            for linha in arquivo:

                # Remove as quebras de linha do arquivo
                linha = re.sub('\n|\r', '', linha).strip()

                # Remove os comentarios das linhas
                if '//' in linha:
                    linha = linha.split('//')[0]

                # Identifica qual a forma de leitura (sentença/gramatica/linha em branco/comentario)
                if '::=' in linha:
                    if not modo_gramatica:
                        gramatica = Gramatica()

                    modo_gramatica = True

                    gramatica.add_simbolo(
                        decodificar_gramatica(
                            linha, gramatica.get_simbolos_nao_terminais()
                        )
                    )

                elif linha != '':
                    gramatica = decodificar_sentenca(linha)

                else:
                    modo_gramatica = False

                # No caso de estar lendo uma gramática, insere apenas no final
                if not modo_gramatica and gramatica.get_simbolos() != []:
                    gramaticas.append(gramatica)
                    gramatica = Gramatica([])

            # Caso chegue no final do arquivo com uma gramática em aberto
            if modo_gramatica:
                gramaticas.append(gramatica)

    except Exception as e:
        print('Erro ao ler arquivo da linguagem. ' + str(e))
        exit()

    return gramaticas


# Decodifica o texto da sentença e retorna elementos
def decodificar_sentenca(sentenca: str):
    # Gera símbolos não terminais em ordem alfabética
    gerador_nao_terminal = gerador_de_tokens()

    # Armazena os símbolos de controle
    atual = SimboloNaoTerminal('S', True)

    gramatica = Gramatica()

    # Gera uma nova gramática para cada símbolo da sentença
    for simbolo in sentenca:
        proximo = SimboloNaoTerminal(next(gerador_nao_terminal))
        atual.producao.add_regra(Regra([SimboloTerminal(simbolo), proximo]))
        gramatica.add_simbolo(atual)
        atual = proximo

    # Insere a produção final na gramática (contendo apenas epsilon)
    atual.producao.add_regra(
        Regra([Epsilon()], sentenca)
    )
    gramatica.add_simbolo(atual)

    return gramatica


# Decodifica a string da gramática e retorna elementos
def decodificar_gramatica(str_gramatica: str, simbolos_da_gramatica=None):
    # Separa o não-terminal das produções
    if simbolos_da_gramatica is None:
        simbolos_da_gramatica = set()
    [simbolo, regras] = str_gramatica.split('::=')
    simbolo = re.search('<(.*?)>', simbolo).group(1)
    simbolo = SimboloNaoTerminal(simbolo, simbolo == 'S')

    for s in simbolos_da_gramatica:
        if s.get_caracter() == simbolo.get_caracter():
            simbolo = s

    simbolos_da_gramatica.add(simbolo)

    # Identifica as regras das produções
    for str_regra in regras.split('|'):

        reconhecedor = None

        # Se a regra reconhece algum token
        if '%' in str_regra:
            str_regra, reconhecedor = str_regra.split('%', 1)
            reconhecedor = reconhecedor.split('%')[0].strip()

        str_regra = str_regra.strip()

        # Identifica os símbolos da regra
        regra = Regra([], reconhecedor)
        while str_regra:

            str_simbolo = str_regra[0]

            # Identifica símbolo não-terminal
            if str_simbolo == '<':
                str_regra = str_regra[1:].split('>', 1)
                nao_terminal = SimboloNaoTerminal(str_regra[0])

                for s in simbolos_da_gramatica:
                    if s.get_caracter() == nao_terminal.get_caracter():
                        nao_terminal = s
                        break

                simbolos_da_gramatica.add(nao_terminal)
                regra.add_simbolo(nao_terminal)
                str_regra = str_regra[1]

            else:
                # Identifica símbolo épsilon
                if str_simbolo == 'ε':
                    regra.add_simbolo(Epsilon())

                # Identifica símbolo terminal
                elif str_simbolo != ' ':
                    regra.add_simbolo(SimboloTerminal(str_simbolo))

                str_regra = str_regra[1:]

        simbolo.get_producao().add_regra(regra)

    return simbolo


if __name__ == '__main__':
    print(ler_linguagem('../arquivos/linguagem.txt'))
