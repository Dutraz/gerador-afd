from copy import copy

from src.reconhecedor.tabela_simbolos.simbolo import Simbolo
from src.reconhecedor.tabela_simbolos.tabela import Tabela


class AnalisadorSemantico:

    def __init__(self, tabela_simbolos: Tabela):
        self.tabela_simbolos = tabela_simbolos

    def realizar_acoes(self, acoes: list[str], desempilhados: list[Simbolo], reconhecido: Simbolo, gera_temp):
        retorno = {'sucesso': True, 'mensagem': ''}

        desempilhados_copia = [copy(d) for d in desempilhados]

        for acao in acoes:
            r = self.realizar_acao(acao, desempilhados, desempilhados_copia, reconhecido, gera_temp)
            if not r['sucesso']:
                retorno['sucesso'] = False
                retorno['mensagem'] += r['mensagem']

        return retorno

    def realizar_acao(self, acao: str, desempilhados: list[Simbolo], desempilhados_copia, reconhecido: Simbolo, gerador_temp):
        # Reconhece os parâmtros e seus atributos
        funcao = acao.split('(')[0]
        parametros = [
            {'simbolo': s.split('.')[0].strip(), 'atributo': s.split('.')[1].strip()} if '.' in s else s.strip()
            for s in acao.replace(funcao, '').strip()[1:-1].split(',')
        ]

        if 'addTS' in acao:
            # Separa os parametros
            destino, fonte = parametros

            # Verifica se é um valor absoluto
            if isinstance(fonte, str):
                atributo = fonte
            else:
                # Encontra quem é o simbolo fonte
                simbolo_fonte = self.encontrar_simbolo(acao, desempilhados, reconhecido, fonte['simbolo'])
                atributo = simbolo_fonte.get_atributo(fonte['atributo'])

            # Encontra o simbolo destino e guarda o novo atributo
            simbolo_destino = self.encontrar_simbolo(acao, desempilhados, reconhecido, destino['simbolo'])
            simbolo_destino.set_atributo(destino['atributo'], atributo)

        elif 'verifica' in acao:
            p1, p2 = parametros

            # Encontra os símbolos
            s1 = self.encontrar_simbolo(acao, desempilhados, reconhecido, p1['simbolo'])
            s2 = self.encontrar_simbolo(acao, desempilhados, reconhecido, p2['simbolo'])

            if s1.get_atributo('tipo') != s2.get_atributo('tipo'):
                return {
                    'sucesso': False,
                    'mensagem': f'Tipos incompatíveis ({s1.get_atributo("tipo")} e {s2.get_atributo("tipo")})'
                }

        elif 'geraTemp' in acao:
            destino = parametros[0]
            simbolo_destino = self.encontrar_simbolo(acao, desempilhados, reconhecido, destino['simbolo'])
            simbolo_destino.set_atributo('valor_lexico', next(gerador_temp))

        elif 'geraCod' in acao:
            print(acao)
            codigo_intermediario = ''

            # Concatena todos os parametros da funcao
            for param in parametros:
                # Verifica se é um valor absoluto e pega o valor dentro das aspas
                if isinstance(param, str):
                    codigo = param[1:-1]
                else:
                    simbolo_fonte = self.encontrar_simbolo(acao, desempilhados_copia, reconhecido, param['simbolo'])
                    codigo = simbolo_fonte.get_atributo(param['atributo'])

                codigo_intermediario += codigo

            reconhecido.set_atributo('codigo', codigo_intermediario)
            print(codigo_intermediario)

        else:
            print(f'\n\n!!! Erro ao realizar acao {acao}, acao não reconhecida.\n')
            exit()

        return {
            'sucesso': True,
        }

    @staticmethod
    def encontrar_simbolo(acao: str, simbolos: list[Simbolo], reconhecido: Simbolo, simbolo: str):
        try:
            # Caso seja uma operação com o símbolo que dá nome à regra reconhecida
            if '*' in simbolo:
                if simbolo.replace('*', '') != reconhecido.get_valor_sintatico():
                    print(f'\n\n!!! Erro ao realizar acao {acao}, nome do símbolo que dá nome a regra não confere.\n')
                    exit()
                return reconhecido

            # Caso seja uma operação com um dos simbolos da regra
            return [s for s in simbolos if s.get_valor_sintatico() == simbolo][0]

        except IndexError:
            print(f'\n\n!!! Erro ao realizar acao {acao}, simbolos não encontrados.\n')
            exit()
