from src.linguagem.automato.estado import Estado
from src.linguagem.gramatica.gramatica import Gramatica
from src.linguagem.gramatica.simbolo import SimboloNaoTerminal
from prettytable import PrettyTable


class Automato:

    # Construtor do Autômato
    def __init__(self, arg):
        # Se o argumento for uma lista de estados
        if (arg is list[Estado]):
            self.estados = arg
        # Se o argumento for uma gramática
        else:
            self.estados = self.__carregarGramatica(arg[0])

    # Chamado implicitamente no print
    def __str__(self):
        # Busca os terminais de todos os estados
        terminais = set()
        for estado in self.estados:
            if (estado.getTransicoes()):
                terminais.update(
                    estado.getTransicoes().keys()
                )
        terminais = sorted(terminais)

        # Monta as linhas da tabela em um array
        linhas = []
        for estado in self.estados:
            # Insere na primeira célula da linha o não-terminal
            linha = [estado.getIdentificador()]
            linhas.append(linha)

            # Insere as transições de cada um dos terminais (se houverem)
            for terminal in terminais:
                if terminal in estado.getTransicoes():
                    # Insere a transição no formato '[A,B]' na célula
                    linha.append(estado.getTransicaoPor(terminal))
                else:
                    linha.append('')

        # Instancia a tabela e adiciona as linhas
        tabela = PrettyTable(list(['-', *terminais]))
        tabela.add_rows(sorted(linhas, key=lambda e: e[0]))
        return str(tabela)

    # Adicionar novo estado ao autômato
    def addEstado(self, estado: Estado):
        self.estados.append(estado)
        return self

    # Remover estado do autômato
    def rmEstado(self, estado: Estado):
        self.estados.remove(estado)
        return self

    # Pegar o estado pelo símbolo (se houver)
    def getEstado(self, simbolo):
        if (simbolo in self.estados):
            return self.estados[self.estados.index(simbolo)]

    # Pegar o estado inicial
    def getEstadoInicial(self):
        for estado in self.estados:
            if estado.isInicial():
                return estado

    def getEstadoErro(self):
        for estado in self.estados:
            if estado.isErro():
                return estado

    # Determinizar o Autômato Finito (AFD -> AFND)
    def determinizar(self):
        # Inicializa o novo array de estados apenas com o estado incial
        estados = [e for e in self.estados if e.isInicial()]

        # Itera sobre o novo array de estados buscando transições não verificadas
        # (desta forma já eliminamos a existência de estados inalcançáveis)
        for estado in estados:
            for terminal in estado.transicoes:
                # Pega o estado alcançável por um terminal
                transicao = estado.getTransicaoPor(terminal)

                # Verifica se já há algum estado com os caracteres
                if transicao not in estados:
                    estados.append(transicao)

        # Torna os novos estados, os estados da classe
        self.estados = estados

    # Apenas remover estados mortos
    def minimizar(self):
        # Inicializando os conjuntos de cada estado
        for estado in self.estados:
            if estado.ehMorto([]):
                self.rmEstado(estado)

        for estado in self.estados:
            for terminal in list(estado.getTransicoes()):
                if estado.getTransicoes()[terminal] not in self.estados:
                    del estado.getTransicoes()[terminal]

    def inserirEstadoErro(self):
        # Busca os terminais de todos os estados
        terminais = set()
        for estado in self.estados:
            if (estado.getTransicoes()):
                terminais.update(
                    estado.getTransicoes().keys()
                )

        erro = Estado(
            {SimboloNaoTerminal('_')},
            False,
            True,
            True
        )
        self.addEstado(erro)
        for estado in self.estados:
            for terminal in terminais:
                if not estado.getTransicaoPor(terminal):
                    estado.addTransicao(terminal, erro)

    # Transforma uma gramática em um array de estados
    def __carregarGramatica(self, gramatica: Gramatica) -> list[Estado]:

        # Função auxiliar para gerar tabela não terminais
        geradorNaoTerminal = (
            SimboloNaoTerminal(chr(i)) for i in range(ord('A'), ord('Z'))
        )

        # Inicializa o conjunto de estados apenas com o inicial
        inicial = Estado(
            {s for s in gramatica.getSimbolos() if s.getCaracter() == 'S'},
            True
        )

        # Todos os estados do automato (AFND e AFD)
        verificar = [inicial]

        # Estados para o AFND
        estados = [inicial]

        # Itera sobre os símbolos da gramática e transforma-os em estados
        for estado in verificar:
            for simbolo in estado.getNaoTerminais():
                for regra in simbolo.getProducao().getRegras():
                    estado.setFinal(estado.isFinal() or regra.isFinal())

                    # Cria transições para cada regra não-terminal da gramática
                    if not regra.isFinal():
                        # Filtra os não-terminais da regra
                        naoTerminais = regra.getSimbolosNaoTerminais()

                        # Caso em que a regra é composta por apenas símbolos terminais
                        # deve ser levado a uma nova regra (final)
                        while not naoTerminais:
                            novoNaoTerminal = next(geradorNaoTerminal)
                            if novoNaoTerminal not in gramatica.getSimbolos():
                                gramatica.addSimbolo(novoNaoTerminal)
                                naoTerminais = {novoNaoTerminal}

                        terminais = ''.join(
                            [
                                s.getCaracter() for s in regra.getSimbolosTerminais()
                            ] or 'ε'
                        )

                        novaTransicao = Estado(
                            naoTerminais,
                            False,
                            regra.isFinal() or not regra.getSimbolosNaoTerminais()
                        )

                        if novaTransicao in verificar:
                            novaTransicao = verificar[verificar.index(novaTransicao)]
                        else:
                            verificar.append(novaTransicao)
                            estados.append(novaTransicao)

                        transicao = estado.getTransicaoPor(terminais)
                        if transicao is None:
                            # Adiciona transição ao dicionário (a:Estado(A,B))
                            estado.addTransicao(
                                terminais,
                                novaTransicao
                            )
                        elif transicao != novaTransicao:

                            # Criar novo estado com ambas as transições
                            composto = Estado(
                                set(transicao.getNaoTerminais()),
                                False,
                                regra.isFinal()
                            )
                            composto.addNaoTerminais(regra.getSimbolosNaoTerminais())

                            # Verifica se o estado já foi criado e está na fila verificação
                            if composto in verificar:
                                composto = verificar[verificar.index(composto)]

                            # Associar novo estado à transição
                            estado.getTransicoes()[terminais] = composto

                            if composto not in verificar:
                                verificar.append(composto)

        return estados
