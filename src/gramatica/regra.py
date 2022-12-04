class Regra:

    def __init__(self, simbolos = []):
        self.simbolos = simbolos

    def __str__(self):
        return ''.join([str(s) for s in self.simbolos])

    def addSimbolo(self, simbolo):
        self.simbolos.append(simbolo)
        return self
