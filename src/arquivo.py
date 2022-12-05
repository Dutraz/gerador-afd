import re

from linguagem.simbolo import SimboloNaoTerminal
from linguagem.linguagem import Linguagem
from linguagem.gramatica import Gramatica


def lerEntrada(path: str):

    linguagem = Linguagem()

    try:
        with open(path, encoding='utf-8') as arquivo:

            # Flag indicando se esta no meio da leitura de uma gramática
            gramatica = Gramatica([])
            modo_gramatica = False

            for linha in arquivo:

                # Remove as quebras de linha da string
                linha = re.sub('\n|\r', '', linha).strip()

                # Identifica qual o tipo de leitura (sentença/gramatica/linha em branco)
                if ('::=' in linha):
                    gramatica.addSimbolo(
                        SimboloNaoTerminal().porGramatica(linha)
                    )
                    modo_gramatica = True
                elif (linha != ''):
                    gramatica = gramatica.porSentenca(linha)
                else:
                    modo_gramatica = False

                # No caso de estar lendo uma gramática, insere apenas no final
                if (modo_gramatica == False and gramatica.getSimbolos() != []):
                    linguagem.addGramatica(gramatica)
                    gramatica = Gramatica([])

            # Caso chegue no final do arquivo com uma gramática em aberto
            if (modo_gramatica == True and gramatica.getSimbolos() != []):
                linguagem.addGramatica(gramatica)

    except Exception as e:
        print('Erro ao ler arquivo de log. ' + str(e))
        exit()

    return linguagem


if __name__ == '__main__':
    print(lerEntrada('../arquivos/entrada.txt'))
