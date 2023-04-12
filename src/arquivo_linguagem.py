import re

from linguagem.gramatica.gramatica import Gramatica
from linguagem.gramatica.regra import Regra
from linguagem.gramatica.simbolo import SimboloNaoTerminal, SimboloTerminal, Epsilon


def ler_linguagem(path: str):
    gramaticas = []

    try:
        with open(path, encoding='utf-8') as arquivo:

            # Flag indicando se esta no meio da leitura de uma gramática
            gramatica = Gramatica()
            modo_gramatica = False

            for linha in arquivo:

                # Remove as quebras de linha da string
                linha = re.sub('\n|\r', '', linha).strip()

                # Remove os comentarios das linhas
                if ('//' in linha):
                    linha = linha.split('//')[0]

                # Identifica qual o tipo de leitura (sentença/gramatica/linha em branco/comentario)
                if ('::=' in linha):
                    if (modo_gramatica == False):
                        gramatica = Gramatica()

                    modo_gramatica = True

                    gramatica.addSimbolo(
                        decodificarGramatica(
                            linha, gramatica.getSimbolosNaoTerminais()
                        )
                    )

                elif (linha != ''):
                    gramatica = decodificarSentenca(linha)

                else:
                    modo_gramatica = False

                # No caso de estar lendo uma gramática, insere apenas no final
                if (modo_gramatica == False and gramatica.getSimbolos() != []):
                    gramaticas.append(gramatica)
                    gramatica = Gramatica([])

            # Caso chegue no final do arquivo com uma gramática em aberto
            if (modo_gramatica == True):
                gramaticas.append(gramatica)

    except Exception as e:
        print('Erro ao ler arquivo de log. ' + str(e))
        exit()

    return gramaticas


# Decodifica a string da sentença e retorna elementos
def decodificarSentenca(sentenca: str):
    # Gera símbolos não terminais em ordem alfabética
    naoTerminal = (
        SimboloNaoTerminal(chr(i)) for i in range(ord('A'), ord('Z'))
    )

    # Armazena os símbolos de controle
    atual = SimboloNaoTerminal('S', True)
    proximo = None

    gramatica = Gramatica()

    # Gera uma nova gramática para cada símbolo da sentença
    for simbolo in sentenca:
        proximo = next(naoTerminal)
        atual.producao.addRegra(Regra([SimboloTerminal(simbolo), proximo]))
        gramatica.addSimbolo(atual)
        atual = proximo

    # Insere a produção final na gramática (contendo apenas epsilon)
    atual.producao.addRegra(Regra([Epsilon()]))
    gramatica.addSimbolo(atual)

    return gramatica


# Decodifica a string da gramática e retorna elementos
def decodificarGramatica(strGramatica: str, simbolosDaGramatica: set = set()):
    # Separa o não-terminal das produções
    [simbolo, regras] = strGramatica.split('::=')
    simbolo = re.search('<(.*?)>', simbolo).group(1)
    simbolo = SimboloNaoTerminal(simbolo, simbolo == 'S')

    for s in simbolosDaGramatica:
        if (s.getCaracter() == simbolo.getCaracter()):
            simbolo = s

    simbolosDaGramatica.add(simbolo)

    # Identifica as regras das produções
    for strRegra in regras.split('|'):
        strRegra = strRegra.strip()

        # Identifica os símbolos da regra
        regra = Regra([])
        while strRegra:

            strSimbolo = strRegra[0]

            # Identifica símbolo não-terminal
            if strSimbolo == '<':
                strRegra = strRegra[1:].split('>', 1)
                naoTerminal = SimboloNaoTerminal(strRegra[0])

                for s in simbolosDaGramatica:
                    if (s.getCaracter() == naoTerminal.getCaracter()):
                        naoTerminal = s
                        break

                simbolosDaGramatica.add(naoTerminal)
                regra.addSimbolo(naoTerminal)
                strRegra = strRegra[1]

            else:
                # Identifica símbolo épsilon
                if strSimbolo == 'ε':
                    regra.addSimbolo(Epsilon())

                # Identifica símbolo terminal
                elif strSimbolo != ' ':
                    regra.addSimbolo(SimboloTerminal(strSimbolo))

                strRegra = strRegra[1:]

        simbolo.getProducao().addRegra(regra)

    return simbolo


if __name__ == '__main__':
    print(ler_linguagem('../arquivos/linguagem.txt'))
