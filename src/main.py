from arquivo import lerEntrada
from linguagem.automato.automato import Automato
from linguagem.linguagem import Linguagem


def main():
    linguagem = Linguagem() 
    linguagem.setGramaticas(lerEntrada('../arquivos/entrada.txt'))
    linguagem.gerarAutomato()

    # print(linguagem.getAutomato())
    print(linguagem)

if __name__ == '__main__':
    main()
