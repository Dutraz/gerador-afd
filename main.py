import os

from src.arquivo_fonte import ler_fonte
from src.arquivo_linguagem import ler_linguagem
from src.linguagem.linguagem import Linguagem
from src.reconhecedor.lexico import AnalisadorLexico


def main():
    os.system('cls')

    print('\nRECONHECENDO SENTENÇAS E GRAMÁTICAS...\n')
    linguagem = Linguagem()
    linguagem.setGramaticas(ler_linguagem('arquivos/linguagem.txt'))
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

    print('\n\n\n\n')
    print('============================================')
    print('======== CARREGANDO CÓDIGO FONTE... ========')
    print('============================================\n')
    analisador_lexico = AnalisadorLexico(
        linguagem,
        ler_fonte('arquivos/fonte.txt')
    )

    print('\nCRIANDO FITA DE LEITURA...\n')
    print(analisador_lexico.get_fita(), end="\n\n=============\n\n")

    print('\nCRIANDO TABELA DE SÍMBOLOS...\n')
    print(analisador_lexico.get_tabela(), end="\n\n=============\n\n")

    print(analisador_lexico.get_erros())


if __name__ == '__main__':
    main()
