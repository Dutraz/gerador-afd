import os

from arquivo_fonte import ler_fonte
from arquivo_linguagem import ler_linguagem
from linguagem.linguagem import Linguagem
from reconhecedor.tabela.tabela import Tabela


def main():
    os.system('cls')

    print('\nRECONHECENDO SENTENÇAS E GRAMÁTICAS...\n')
    linguagem = Linguagem()
    linguagem.setGramaticas(ler_linguagem('../arquivos/linguagem.txt'))
    print(linguagem, end="\n\n=============\n\n")

    print('\nUNIFICANDO GRAMÁTICAS...\n')
    linguagem.setGramaticas([linguagem.unificarGramaticas()])
    print(linguagem, end="\n\n=============\n\n")

    print('\nREMOVENDO EPSILON TRANSIÇÕES...\n')
    linguagem.setGramaticas(linguagem.rmEpsilonTransicoes())
    print(linguagem, end="\n\n=============\n\n")

    print('\nGERANDO AUTÔMATO FINITO...\n')
    linguagem.gerarAutomato()
    print(linguagem.getAutomato(), end="\n\n=============\n\n")

    print('\nDETERMINIZANDO AUTOMATO FINITO...\n')
    linguagem.getAutomato().determinizar()
    print(linguagem.getAutomato(), end="\n\n=============\n\n")

    print('\nMINIMIZANDO AUTOMATO FINITO...\n')
    linguagem.getAutomato().minimizar()
    print(linguagem.getAutomato(), end="\n\n=============\n\n")

    print('\nINSERINDO ESTADO DE ERRO...\n')
    linguagem.getAutomato().inserirEstadoErro()
    print(linguagem.getAutomato(), end="\n\n=============\n\n")

    print('\nCARREGANDO CÓDIGO FONTE...\n')
    tabela = Tabela(ler_fonte('../arquivos/fonte.txt'))
    print(tabela)


if __name__ == '__main__':
    main()
