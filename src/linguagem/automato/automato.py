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
            self.estados = self.__carregarGramatica(argumento[0])

    def __str__(self):

        terminais = set()

        for e in self.estados:
            if (e.getTransicoes()):
                terminais.update(e.getTransicoes().keys())

        terminais = sorted(terminais)
        # naoTerminais = sorted(self.estados, key=Estado.estado)

        linhas = []

        for e in self.estados:

            transicoes = e.getTransicoes()
            linha = [str(e)]

            for terminal in terminais:
                if terminal in transicoes:
                    linha.append(
                        f'[{",".join([t.getCaracter() for t in transicoes[terminal]])}]')
                else:
                    linha.append('')

            linhas.append(linha)

        tab = PrettyTable(list(['-', *terminais]))
        tab.add_rows(linhas)
        return str(tab)

    def addEstado(self, estado: Estado):
        self.estados.append(estado)
        return self

    # Transforma uma gramática em um array de estados
    def __carregarGramatica(self, gramatica: Gramatica):

        simboloInicial = next(filter(
            lambda x: x.isInicial(), gramatica.getSimbolos()
        ))

        estados = []
        simbolosVerificar = {simboloInicial}

        while simbolosVerificar != set():

            simbolo = simbolosVerificar.pop()
            estado = Estado(simbolo).setInicial(simbolo.getCaracter() == 'S')

            regras = simbolo.getProducao().getRegras()

            if (regras == []):
                estado.setFinal()
            else:
                for regra in regras:

                    terminais = [
                        str(s) for s in regra.getSimbolos() if isinstance(s, SimboloTerminal)
                    ]

                    naoTerminais = [
                        s for s in regra.getSimbolos() if isinstance(s, SimboloNaoTerminal)
                    ]

                    if (isinstance(regra.getSimbolos()[0], Epsilon)):
                        estado.setFinal()
                    else:
                        estado.addTransicao(
                            ''.join(terminais), set(naoTerminais)
                        )

                    if (simbolo in naoTerminais):
                        naoTerminais.remove(simbolo)

                    simbolosVerificar.update(naoTerminais)

            estados.append(estado)

        return estados
