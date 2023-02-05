from linguagem.automato.estado import Estado
from linguagem.gramatica.gramatica import Gramatica
from linguagem.gramatica.simbolo import SimboloTerminal, SimboloNaoTerminal, Epsilon
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
            linha = [str(estado)]
            linhas.append(linha)

            # Insere as transições de cada um dos terminais (se houverem)
            for terminal in terminais:
                if terminal in estado.getTransicoes():
                    # Insere a transição no formato '[A,B]' na célula
                    linha.append(
                        '[' + (
                            ",".join(
                                sorted(
                                    [t.getCaracter()
                                     for t in estado.getTransicoes()[terminal]
                                     ]
                                )
                            )
                        ) + ']'
                    )
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

    # Determinizar o Autômato Finito (AFD -> AFND)
    def determinizar(self):
        # Inicializa o novo array de estados apenas com o estado incial
        estados = [e for e in self.estados if e.isInicial()]

        # Itera sobre o novo array de estados buscando transições não verificadas
        # (desta forma já eliminamos a existência de estados inalcançáveis)
        for estado in estados:
            for transicao in estado.transicoes:
                # Pega todas as possíveis transições alcançáveis por um terminal
                transicoes = estado.transicoes[transicao]

                # Monta a string referente à transição como: 'A,B'
                caracteres = ','.join(
                    sorted(
                        [t.getCaracter() for t in transicoes]
                    )
                )

                # Verifica se já há algum estado com os caracteres
                if caracteres not in estados:
                    # Se não houver, cria um novo estado com eles
                    novoestado = Estado(SimboloNaoTerminal(caracteres))
                    estados.append(novoestado)

                    # Para cada símbolo da transição
                    for simbolo in transicoes:
                        s = self.getEstado(simbolo)
                        # Agrupa as transições de cada um deles
                        for novatransicao in s.getTransicoes():
                            novoestado.addTransicao(
                                novatransicao,
                                s.getTransicoes()[novatransicao]
                            )
                        # Aproveita para passar se é estado final
                        if (s.isFinal()):
                            novoestado.setFinal()

        # Torna os novos estados, os estados da classe
        self.estados = estados

    # Apenas remover estados mortos
    def minimizar(self):
        # Inicializando os conjuntos de cada estado
        for estado in self.estados:
            ehMorto = True
            if estado.isFinal():
                ehMorto = False
            else:
                verificados = set()
                for transicao in {t for tr in estado.getTransicoes().values() for t in tr}:
                    if (transicao not in verificados):
                        if (self.getEstado(transicao)):
                            if (self.getEstado(transicao).isFinal()):
                                ehMorto = False
                        verificados.add(transicao)
            if (ehMorto):
                self.rmEstado(estado)
                for e in self.estados:
                    for transicao in list(e.getTransicoes()):
                        if (estado.getCaracteres() == ','.join([s.getCaracter() for s in e.getTransicoes()[transicao]])):
                            if (estado.getCaracteres() in e.getTransicoes()[transicao]):
                                e.getTransicoes()[transicao].remove(
                                    estado.getCaracteres()
                                )
                        if (e.getTransicoes()[transicao] == set()):
                            del e.getTransicoes()[transicao]

    # Transforma uma gramática em um array de estados
    def __carregarGramatica(self, gramatica: Gramatica) -> list[Estado]:

        # Função auxiliar para gerar simbolos não terminais
        geradorNaoTerminal = (
            SimboloNaoTerminal(chr(i)) for i in range(ord('A'), ord('Z'))
        )

        # Itera sobre os símbolos da gramática e transforma-os em estados
        estados = []
        for simbolo in gramatica.getSimbolos():
            # Instancia o símbolo já indicando se é inicial (igual a S)
            estado = Estado(simbolo).setInicial(
                simbolo.getCaracter() == 'S'
            )
            estados.append(estado)

            # Itera sobre as regras do símbolo
            for regra in simbolo.getProducao().getRegras():
                estado.setFinal(regra.isFinal())

                # Cria novas transições para cada regra da gramática
                if (not estado.isFinal()):
                    # Caso for EPSILON
                    if (isinstance(regra.getSimbolos()[0], Epsilon)):
                        estado.setFinal()
                    else:
                        # Filtra os não-terminais da regra
                        naoTerminais = [
                            s for s in regra.getSimbolos() if isinstance(s, SimboloNaoTerminal)
                        ]

                        # Caso em que a regra é composta por apenas símbolos terminais
                        # deve ser levado a uma nova regra (final)
                        if (naoTerminais == []):
                            while naoTerminais == []:
                                novoNaoTerminal = next(geradorNaoTerminal)
                                if (novoNaoTerminal not in gramatica.getSimbolos()):
                                    gramatica.addSimbolo(novoNaoTerminal)
                                    naoTerminais = [novoNaoTerminal]

                        # Adiciona transição ao dicionário (a:[A,B])
                        estado.addTransicao(
                            ''.join([
                                s.getCaracter() for s in regra.getSimbolosTerminais()
                            ]), regra.getSimbolosNaoTerminais()
                        )

        return estados
