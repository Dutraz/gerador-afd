from linguagem.regra import Regra


class Producao:

    def __init__(self, regras: list[Regra] = []):
        self.regras = regras

    def __str__(self):
        return ' | '.join([str(r) for r in self.regras])

    def addRegra(self, regra: Regra):
        self.regras.append(regra)
        return self

    # Preenche as regras da produção a partir de uma gramática
    def porGramatica(self, gramatica: str):
        self.regras = [
            Regra().porGramatica(regra) for regra in gramatica.split('|')
        ]
        return self
