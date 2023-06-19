import os

from src.arquivo_estrutura import ler_estruturas
from src.arquivo_fonte import ler_fonte
from src.arquivo_linguagem import ler_linguagem
from src.linguagem.linguagem import Linguagem
from src.reconhecedor.lexico import AnalisadorLexico
from src.reconhecedor.sintatico import AnalisadorSintatico


def main():
    os.system('cls')

    print('\nRECONHECENDO SENTENÇAS E GRAMÁTICAS...\n')
    linguagem = Linguagem()
    linguagem.set_gramaticas(ler_linguagem('arquivos/linguagem.txt'))
    print(linguagem, end="\n\n=============\n\n")

    print('\nUNIFICANDO GRAMÁTICAS...\n')
    linguagem.set_gramaticas([linguagem.unificar_gramaticas()])
    print(linguagem, end="\n\n=============\n\n")

    print('\nREMOVENDO EPSILON TRANSIÇÕES...\n')
    linguagem.set_gramaticas(linguagem.remover_epsilon_transicoes())
    print(linguagem, end="\n\n=============\n\n")

    print('\nGERANDO AUTÔMATO FINITO...\n')
    linguagem.gerar_automato()
    print(linguagem.get_automato(), end="\n\n=============\n\n")

    print('\nDETERMINIZANDO AUTOMATO FINITO...\n')
    linguagem.get_automato().determinizar()
    print(linguagem.get_automato(), end="\n\n=============\n\n")

    print('\nMINIMIZANDO AUTOMATO FINITO...\n')
    linguagem.get_automato().minimizar()
    print(linguagem.get_automato(), end="\n\n=============\n\n")

    print('\nINSERINDO ESTADO DE ERRO...\n')
    linguagem.get_automato().inserir_estado_erro()
    print(linguagem.get_automato(), end="\n\n=============\n\n")

    print('\n\n\n\n')
    print('============================================')
    print('======== CARREGANDO CÓDIGO FONTE... ========')
    print('============================================\n')
    analisador_lexico = AnalisadorLexico(
        linguagem,
        ler_fonte('arquivos/fonte.txt')
    )

    print('\nCRIANDO FITA DE LEITURA...\n')
    print(analisador_lexico.get_str_fita(), end="\n\n=============\n\n")

    print('\nCRIANDO TABELA DE SÍMBOLOS...\n')
    print(analisador_lexico.get_tabela(), end="\n\n=============\n\n")
    print(analisador_lexico.get_erros())

    print('\n\n\n\n')
    print('============================================')
    print('====== CARREGANDO TABELA DE ANÁLISE... =====')
    print('============================================\n')
    analisador_sintatico = AnalisadorSintatico(
        linguagem,
        ler_estruturas('arquivos/estruturas.txt'),
        analisador_lexico.get_fita()
    )
    print(analisador_sintatico.get_tabela_analise())

    print('\nANALISANDO SINTATICAMENTE CÓDIGO FONTE...\n')
    analisador_sintatico.verificar()


if __name__ == '__main__':
    main()
