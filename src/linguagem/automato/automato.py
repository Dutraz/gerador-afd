from prettytable import PrettyTable

from src.linguagem.automato.estado import Estado
from src.linguagem.gramatica.gramatica import Gramatica
from src.linguagem.gramatica.simbolo import SimboloNaoTerminal


class Automato:

    # Construtor do Autômato
    def __init__(self, arg):
        # Se o argumento for uma lista de estados
        if arg is list[Estado]:
            self.estados = arg
        # Se o argumento for uma gramática
        else:
            self.estados = self.__carregar_gramatica(arg[0])

    # Chamado implicitamente no impressao
    def __str__(self):
        # Busca os terminais de todos os estados
        terminais = set()
        for estado in self.estados:
            if estado.get_transicoes():
                terminais.update(
                    estado.get_transicoes().keys()
                )
        terminais = sorted(terminais)

        # Monta as linhas da tabela em um array
        linhas = []
        for estado in self.estados:
            # Insere na primeira célula da linha o não-terminal
            linha = [estado.get_identificador()]
            linhas.append(linha)

            # Insere as transições de cada um dos terminais (se houverem)
            for terminal in terminais:
                if terminal in estado.get_transicoes():
                    # Insere a transição no formato '[A,B]' na célula
                    linha.append(estado.get_transicao_por(terminal))
                else:
                    linha.append('')

        # Instancia a tabela e adiciona as linhas
        tabela = PrettyTable(list(['-', *terminais]))
        tabela.add_rows(sorted(linhas, key=lambda e: e[0]))
        return str(tabela)

    # Adicionar novo estado ao autômato
    def add_estado(self, estado: Estado):
        self.estados.append(estado)
        return self

    # Remover estado do autômato
    def remover_estado(self, estado: Estado):
        self.estados.remove(estado)
        return self

    # Pegar o estado pelo símbolo (se houver)
    def get_estado(self, simbolo):
        if simbolo in self.estados:
            return self.estados[self.estados.index(simbolo)]

    # Pegar o estado inicial
    def get_estado_inicial(self):
        for estado in self.estados:
            if estado.is_inicial():
                return estado

    def get_estado_erro(self):
        for estado in self.estados:
            if estado.is_erro():
                return estado

    # Determinizar o Autômato Finito (AFD -> AFND)
    def determinizar(self):
        # Inicializa o novo array de estados apenas com o estado incial
        estados = [e for e in self.estados if e.is_inicial()]

        # Itera sobre o novo array de estados buscando transições não verificadas
        # (desta forma já eliminamos a existência de estados inalcançáveis)
        for estado in estados:
            for terminal in estado.transicoes:
                # Pega o estado alcançável por um terminal
                transicao = estado.get_transicao_por(terminal)

                # Verifica se já há algum estado com os caracteres
                if transicao not in estados:
                    estados.append(transicao)

        # Torna os novos estados, os estados da classe
        self.estados = estados

    # Apenas remover estados mortos
    def minimizar(self):
        # Inicializando os conjuntos de cada estado
        for estado in self.estados:
            if estado.is_morto([]):
                self.remover_estado(estado)

        for estado in self.estados:
            for terminal in list(estado.get_transicoes()):
                if estado.get_transicoes()[terminal] not in self.estados:
                    del estado.get_transicoes()[terminal]

    def inserir_estado_erro(self):
        # Busca os terminais de todos os estados
        terminais = set()
        for estado in self.estados:
            if estado.get_transicoes():
                terminais.update(
                    estado.get_transicoes().keys()
                )

        erro = Estado(
            {SimboloNaoTerminal('_')},
            False,
            True,
            True
        )
        self.add_estado(erro)
        for estado in self.estados:
            for terminal in terminais:
                if not estado.get_transicao_por(terminal):
                    estado.add_transicao(terminal, erro)

    # Transforma uma gramática em um array de estados
    @staticmethod
    def __carregar_gramatica(gramatica: Gramatica) -> list[Estado]:

        # Função auxiliar para gerar tabela não terminais
        gerador_nao_terminal = (
            SimboloNaoTerminal(chr(i)) for i in range(ord('A'), ord('Z'))
        )

        # Inicializa o conjunto de estados apenas com o inicial
        inicial = Estado(
            {s for s in gramatica.get_simbolos() if s.get_caracter() == 'S'},
            True
        )

        # Todos os estados do automato (AFND e AFD)
        verificar = [inicial]

        # Estados para o AFND
        estados = [inicial]

        # Itera sobre os símbolos da gramática e transforma-os em estados
        for estado in verificar:
            for simbolo in estado.get_nao_terminais():
                for regra in simbolo.get_producao().get_regras():
                    estado.set_final(estado.is_final() or regra.is_final())

                    # Cria transições para cada regra não-terminal da gramática
                    if not regra.is_final():
                        # Filtra os não-terminais da regra
                        nao_terminais = regra.get_simbolos_nao_terminais()

                        # Caso em que a regra é composta por apenas símbolos terminais
                        # deve ser levado a uma nova regra (final)
                        while not nao_terminais:
                            novo_nao_terminal = next(gerador_nao_terminal)
                            if novo_nao_terminal not in gramatica.get_simbolos():
                                gramatica.add_simbolo(novo_nao_terminal)
                                nao_terminais = {novo_nao_terminal}

                        terminais = ''.join(
                            [
                                s.get_caracter() for s in regra.get_simbolos_terminais()
                            ] or 'ε'
                        )

                        nova_transicao = Estado(
                            nao_terminais,
                            False,
                            regra.is_final() or not regra.get_simbolos_nao_terminais()
                        )

                        if nova_transicao in verificar:
                            nova_transicao = verificar[verificar.index(nova_transicao)]
                        else:
                            verificar.append(nova_transicao)
                            estados.append(nova_transicao)

                        transicao = estado.get_transicao_por(terminais)
                        if transicao is None:
                            # Adiciona transição ao dicionário (a:Estado(A,B))
                            estado.add_transicao(
                                terminais,
                                nova_transicao
                            )
                        elif transicao != nova_transicao:

                            # Cria estado com ambas as transições
                            composto = Estado(
                                set(transicao.get_nao_terminais()),
                                False,
                                regra.is_final()
                            )
                            composto.add_nao_terminais(regra.get_simbolos_nao_terminais())

                            # Verifica se o estado já foi criado e está na fila verificação
                            if composto in verificar:
                                composto = verificar[verificar.index(composto)]

                            # Associar novo estado à transição
                            estado.get_transicoes()[terminais] = composto

                            if composto not in verificar:
                                verificar.append(composto)

        return estados
