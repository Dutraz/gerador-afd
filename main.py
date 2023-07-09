import os

from src.arquivo_estrutura import ler_estruturas, verifica_alteracao
from src.arquivo_fonte import ler_fonte
from src.arquivo_linguagem import ler_linguagem
from src.debug import debug
from src.linguagem.linguagem import Linguagem
from src.reconhecedor.lexico import AnalisadorLexico
from src.reconhecedor.sintatico import AnalisadorSintatico


def main():
    os.system('cls')

    print('\nPROCESSANDO CÓDIGO FONTE...\n')

    debug('\nRECONHECENDO SENTENÇAS E GRAMÁTICAS...\n')
    linguagem = Linguagem()
    linguagem.set_gramaticas(ler_linguagem('arquivos/linguagem.txt'))
    debug(linguagem, True)

    debug('\nUNIFICANDO GRAMÁTICAS...\n')
    linguagem.set_gramaticas([linguagem.unificar_gramaticas()])
    debug(linguagem, True)

    debug('\nREMOVENDO EPSILON TRANSIÇÕES...\n')
    linguagem.set_gramaticas(linguagem.remover_epsilon_transicoes())
    debug(linguagem, True)

    debug('\nGERANDO AUTÔMATO FINITO...\n')
    linguagem.gerar_automato()
    debug(linguagem.get_automato(), True)

    debug('\nDETERMINIZANDO AUTOMATO FINITO...\n')
    linguagem.get_automato().determinizar()
    debug(linguagem.get_automato(), True)

    debug('\nMINIMIZANDO AUTOMATO FINITO...\n')
    linguagem.get_automato().minimizar()
    debug(linguagem.get_automato(), True)

    debug('\nINSERINDO ESTADO DE ERRO...\n')
    linguagem.get_automato().inserir_estado_erro()
    debug(linguagem.get_automato(), True)

    debug('\n\n\n\n')
    debug('============================================')
    debug('======== CARREGANDO CÓDIGO FONTE... ========')
    debug('============================================\n')
    analisador_lexico = AnalisadorLexico(
        linguagem,
        ler_fonte('arquivos/fonte.txt')
    )

    debug('\nCRIANDO FITA DE LEITURA...\n')
    debug(analisador_lexico.get_str_fita(), True)

    debug('\nCRIANDO TABELA DE SÍMBOLOS...\n')
    debug(analisador_lexico.get_tabela(), True)
    verifica_lexico = analisador_lexico.get_erros()
    if verifica_lexico:
        print(verifica_lexico)
        exit()

    debug('\n\n\n\n')
    debug('============================================')
    debug('==== CARREGANDO ESTRUTURAS SINTÁTICAS... ===')
    debug('============================================\n')
    estruturas = ler_estruturas('arquivos/estruturas.txt')

    debug('\nTRADUZINDO O ARQUIVO DE ESTRUTURAS...\n')
    debug('\n'.join([f'|{i:02d}| {e["simbolo"]} -> {e["producao"]}' for i, e in enumerate(estruturas)]))

    debug('\nCARREGANDO TABELA DE ANÁLISE...\n')
    analisador_sintatico = AnalisadorSintatico(
        linguagem,
        estruturas,
        analisador_lexico.get_tabela(),
        verifica_alteracao('arquivos/estruturas.txt'),
    )
    debug(analisador_sintatico.get_tabela_analise(), True)

    debug('\nANALISANDO SINTATICAMENTE CÓDIGO FONTE...\n')
    verificacao_sintatica = analisador_sintatico.verificar()
    debug('\n\n=============\n\n')

    if verificacao_sintatica['sucesso']:
        debug('Código fonte reconhecido sintaticamente.', True)
    else:
        print(verificacao_sintatica['mensagem'], end='\n\n')
        print(verificacao_sintatica['detalhe'], end='\n\n')
        exit()

    print('CÓDIGO RECONHECIDO COM SUCESSO!\n')


if __name__ == '__main__':
    main()
