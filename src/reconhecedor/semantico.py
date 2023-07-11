from src.reconhecedor.tabela_simbolos.simbolo import Simbolo
from src.reconhecedor.tabela_simbolos.tabela import Tabela


class AnalisadorSemantico:

    def __init__(self, tabela_simbolos: Tabela):
        self.tabela_simbolos = tabela_simbolos

    def realizar_acoes(self, acoes: list[str], desempilhados: list[Simbolo], reconhecido: Simbolo):
        retorno = {'sucesso': True, 'mensagem': ''}

        for acao in acoes:
            r = self.realizar_acao(acao, desempilhados, reconhecido)
            if not r['sucesso']:
                retorno['sucesso'] = False
                retorno['mensagem'] += r['mensagem']

        return retorno

    @staticmethod
    def realizar_acao(acao: str, desempilhados: list[Simbolo], reconhecido: Simbolo):
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
                simbolo_fonte = [d for d in desempilhados if d.get_valor_sintatico() == fonte['simbolo']][0]
                atributo = simbolo_fonte.get_atributo(fonte['atributo'])

            # Caso seja uma operação com o símbolo que dá nome à regra reconhecida
            if reconhecido.get_valor_sintatico() == destino['simbolo']:
                simbolo_destino = reconhecido
            else:
                simbolo_destino = [d for d in desempilhados if d.get_valor_sintatico() == destino['simbolo']][0]

            simbolo_destino.set_atributo(destino['atributo'], atributo)

        elif 'verifica' in acao:
            p1, p2 = parametros

            # Encontra os símbolos
            s1 = [d for d in desempilhados if d.get_valor_sintatico() == p1['simbolo']][0]
            s2 = [d for d in desempilhados if d.get_valor_sintatico() == p2['simbolo']][0]

            if s1.get_atributo('tipo') != s2.get_atributo('tipo'):
                return {
                    'sucesso': False,
                    'mensagem': f'Tipos incompatíveis ({s1.get_atributo("tipo")} e {s2.get_atributo("tipo")})'
                }

        return {
            'sucesso': True,
        }
