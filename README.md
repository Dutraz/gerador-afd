# **LOG REDO**

Univeridade Federal da Fronteira Sul — Campus Chapecó

Ciência da Computação — Linguagens Formais e Autômatos II — 2022.2

Prof. Braulio Mello

Acadêmico: **Pedro Zawadzki Dutra**


---


## 💾 **Gerador de Autômatos Finitos Deterministicos**

### **Funcionamento:**
1. O algoritmo recebe como entrada um arquivo de texto com a relação de Tokens e/ou Gramáticas Regulares de uma linguagem.
2. Faz a carga de tokens para a construção de um Autômato Finito Não Determinístico (AFND).
3. Aplicando teoremas de Linguagens Formais e Autômatos, transforma a estrutura em um Autômato Finito Determinístico (AFD), livre de épsilon transições, e mínimo. 


---


## 🚀 **Começando**

### **1. Dependências**
Para executar o projeto você vai precisar:
- [Python 3.x](https://www.python.org/downloads/)

#### 1.1 Instale a biblioteca prettytable

``` powershell
pip install prettytable
```

### **2. Configuração**

Feito a instalação das dependências do projeto, é necessário obter uma cópia do projeto.

Para isso, rode:

``` powershell
git clone --recurse-submodules https://github.com/Dutraz/lfa-gerador-afd && cd lfa-gerador-afd
```

---


## 📋 **Testando:**

Entre na pasta src com o comando:
``` powershell
cd src
```

E então, execute o projeto com:
``` powershell
python main.py
```

---


## 📋 **Descrição:**

Dado um *Arquivo de Entrada* utilizando a notação BNF, como:
```html
se
entao
senao

<S> ::= a<A> | e<A> | i<A> | o<A> | u<A>
<A> ::= a<A> | e<A> | i<A> | o<A> | u<A> | ε
```

O programa deve ser capaz de criar o automato finito:

|  ID  |  s  |  e  |  n  |  t  |  a  |  o  |  i  |  u  |
|------|-----|-----|-----|-----|-----|-----|-----|-----|
|   S  | A,H | C,M |     |     |  M  |  M  |  M  |  M  |
|   A  |     |  B  |     |     |     |     |     |     |
|  *B  |     |     |     |     |     |     |     |     |
|   C  |     |     |  D  |     |     |     |     |     |
|   D  |     |     |     |  E  |     |     |     |     |
|   E  |     |     |     |     |  F  |     |     |     |
|   F  |     |     |     |     |     |  G  |     |     |
|  *G  |     |     |     |     |     |     |     |     |
|   H  |     |  I  |     |     |     |     |     |     |
|   I  |     |     |  J  |     |     |     |     |     |
|   J  |     |     |     |     |  K  |     |     |     |
|   K  |     |     |     |     |     |  L  |     |     |
|  *L  |     |     |     |     |     |     |     |     |
|  *M  |     |  M  |     |     |  M  |  M  |  M  |  M  |

Neste AF exemplo, os estados finais e respectivos tokens são:
- B: se
- G: entao
- L: senao
- M: variavel


Após a construção do AFND, o programa:
- Aplica o teorema de determinização para obter o AFD. 
- O AFD resultante é submetido ao processo de minimização, contudo, sem aplicar Classe de Equivalência.
- Ao final da minimização, é acrescentado um último estado final. Este é o estado de erro. Todas as células da tabela de transição (AFD) não mapeadas agora levam ao estado de erro.
