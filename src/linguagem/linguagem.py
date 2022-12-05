from linguagem.gramatica.gramatica import Gramatica


class Linguagem:

    def __init__(self, gramaticas: list[Gramatica] = []):
        self.gramaticas = gramaticas

    def __str__(self):
        return '\n\n'.join([str(g) for g in self.gramaticas])

    def addGramatica(self, gramatica: Gramatica):
        self.gramaticas.append(gramatica)
        return self
