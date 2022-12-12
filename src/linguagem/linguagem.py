from linguagem.gramatica.simbolo import SimboloNaoTerminal
from linguagem.gramatica.gramatica import Gramatica
from linguagem.automato.automato import Automato


class Linguagem:

    def __init__(self):
        self.gramaticas = []
        self.automato = []

    def __str__(self):
        return '\n\n'.join([str(g) for g in self.gramaticas])

    def setGramaticas(self, gramaticas: list[Gramatica]):
        self.gramaticas = gramaticas
        return self

    def addGramatica(self, gramatica: Gramatica):
        self.gramaticas.append(gramatica)
        return self

    def gerarAutomato(self, gramaticas: list[Gramatica] = []):
        self.automato = Automato(gramaticas or self.gramaticas)
        return self

    def getAutomato(self):
        return self.automato

    def unificarGramaticas(self):
        simboloInicial = SimboloNaoTerminal('S', True)
        g = Gramatica()
        g.addSimbolo(simboloInicial)

        for gramatica in self.gramaticas:
            for simbolo in gramatica.getSimbolos():
                if (simbolo.isInicial()):
                    for regra in simbolo.getProducao().getRegras():
                        simboloInicial.getProducao().addRegra(regra)
                else:
                    while (simbolo.getCaracter() in [s.getCaracter() for s in g.getSimbolos()]):
                        simbolo.setCaracter(
                            chr(ord(simbolo.getCaracter()) + 1)
                        )

                    g.addSimbolo(simbolo)
        return g
