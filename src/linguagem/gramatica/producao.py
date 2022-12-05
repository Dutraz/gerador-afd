from linguagem.gramatica.regra import Regra


class Producao:

    def __init__(self, argumento = []):
        if (argumento is Regra):
            self.regras = list(argumento)
        elif (argumento is list[Regra]):
            self.regras = argumento
        elif (isinstance(argumento, str)):
            self.regras = self.__decodificarGramatica(argumento)
        elif (argumento == []):
            self.regras = []

    def __str__(self):
        return ' | '.join([str(r) for r in self.regras])

    def addRegra(self, regra: Regra):
        self.regras.append(regra)
        return self

    # Decodifica a string da gramática e retorna elementos
    def __decodificarGramatica(self, gramatica: str):
        return [Regra(regra) for regra in gramatica.split('|')]
