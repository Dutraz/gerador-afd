from linguagem.automato.estado import Estado
from linguagem.gramatica.gramatica import Gramatica
from linguagem.gramatica.simbolo import SimboloTerminal, SimboloNaoTerminal


class Automato:

    def __init__(self, argumento):
        if (argumento is list[Estado]):
            self.estados = argumento
        # TODO: Arrumar aqui
        else:
            self.estados = self.__carregarGramatica(argumento)

    def __str__(self):
        return '\n'.join([f'{", ".join(e.naoTerminais)} = {e.getTransicoes()}' for e in self.estados])

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

        # for estado in estados:
        #     print(f'\n{estado} ==== ')
        #     for transicao, estados in estado.getTransicoes().items():
        #         print(f'{transicao}: {", ".join([str(e) for e in estados])}')

