from linguagem.automato.estado import Estado
from linguagem.gramatica.gramatica import Gramatica
from linguagem.gramatica.simbolo import SimboloTerminal, SimboloNaoTerminal, Epsilon
from prettytable import PrettyTable


class Automato:

    def __init__(self, argumento):
        if (argumento is list[Estado]):
            self.estados = argumento
        # TODO: Arrumar aqui
        else:
            self.estados = self.__carregarGramatica(argumento)

    def __str__(self):

        terminais = set()

        for e in self.estados:

            if (e.getTransicoes()):
                terminais.update(e.getTransicoes().keys())

        terminais = list(terminais)

        linhas = []

        for e in self.estados:

            transicoes = e.getTransicoes()
            linha = [f'[{", ".join([s for s in e.getNaoTerminais()])}]']

            for terminal in terminais:
                if terminal in transicoes:
                    linha.append(f'[{", ".join([t.getCaracter() for t in transicoes[terminal]])}]')
                else:
                    linha.append('')

            linhas.append(linha)

        tab = PrettyTable(list(['-', *terminais]))
        tab.add_rows(linhas)
        return str(tab)

    def addEstado(self, estado: Estado):
        self.estados.append(estado)
        return self

    # Transforma um array de gramáticas em um array de estados
    def __carregarGramatica(self, gramaticas: list[Gramatica]):

        inicial = Estado('S')
        simbolosUtilizados = set()

        for gramatica in gramaticas:
            for simbolo in gramatica.getSimbolos():
                if (simbolo.isInicial()):

                    for naoTerminal in simbolo.getProducao().getSimbolosNaoTerminais():
                        while (naoTerminal in simbolosUtilizados):
                            naoTerminal.setCaracter(
                                chr(ord(naoTerminal.getCaracter()) + 1)
                            )

                    for regra in simbolo.getProducao().getRegras():

                        terminais = [
                            str(s) for s in regra.getSimbolos() if isinstance(s, SimboloTerminal)
                        ]

                        naoTerminais = [
                            s for s in regra.getSimbolos() if isinstance(s, SimboloNaoTerminal)
                        ]

                        simbolosUtilizados.update(naoTerminais)

                        if (not isinstance(regra.getSimbolos()[0], Epsilon)):
                            inicial.addTransicao(
                                ''.join(terminais), set(naoTerminais)
                            )

        estados = [inicial]
        simbolosVerificar = simbolosUtilizados.copy()

        while simbolosVerificar != set():

            simbolo = simbolosVerificar.pop()

            if (not simbolo.isInicial()):

                estado = Estado(simbolo.getCaracter())

                for naoTerminal in simbolo.getProducao().getSimbolosNaoTerminais():
                    while (naoTerminal in simbolosUtilizados):
                        naoTerminal.setCaracter(
                            chr(ord(naoTerminal.getCaracter()) + 1)
                        )

                for regra in simbolo.getProducao().getRegras():

                    terminais = [
                        str(s) for s in regra.getSimbolos() if isinstance(s, SimboloTerminal)
                    ]

                    naoTerminais = [
                        s for s in regra.getSimbolos() if isinstance(s, SimboloNaoTerminal)
                    ]

                    estado.addTransicao(
                        ''.join(terminais), set(naoTerminais)
                    )

                    simbolosUtilizados.update(naoTerminais)

                    if (simbolo in naoTerminais):
                        naoTerminais.remove(simbolo)
                    simbolosVerificar.update(naoTerminais)

                estados.append(estado)

        return estados
