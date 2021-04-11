#------------------------------------------------------------------
# O conceito de Nó é implementado como uma classe. Um nó é uma estrutura de dados que,
# nesse contexto, codifica as informações de estado atual, nó pai, ação que o trouxe do
# nó pai e o modelo de transição deste nó para todos seus possíveis filhos.
#
# A classe contém o método de inicialização __init__ (acredito que seja o construtor)
# que define seus atributos fundamentais e atribui a eles os valores recebidos nos argumentos
# durante a declaração do objeto.
#------------------------------------------------------------------

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

#------------------------------------------------------------------
# O conceito de fronteira também é implementado como uma classe.
# Fronteira é o conjunto de nós a serem analisados em dados instante.
# Ou seja, são nós que já foram acessados, mas ainda não foram submetidos
# a teste para validá-los como solução.
#
# Há duas implementações de fronteira: Uma como pilha, outra como fila.
# Cada uma tem sua vantajem. No caso de pilha, o algoritmo realiza primeiro
# uma busca até o fim de um ramo. Já para fila, a busca é feita igualmente
# alternadamente entre os ramos do grafo.
#
# No problema Degrees, como pretendo implementar uma Breadth First Search,
# utilizarei a implementação da fronteira como fila.
#------------------------------------------------------------------

class StackFrontier():
    # O atributo frontier é uma lista comum do Python.
    def __init__(self):
        self.frontier = []

    # Este método adiciona ao fim da fronteira (Uma lista) o nó especificado no argumento.
    # (Lembrando que o nó é um objeto.)
    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def isEmpty(self):
        return len(self.frontier) == 0


    # Retira o último nó da fronteira.
    def remove(self):
        if self.isEmpty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    # Retira o primeiro nó da fronteira
    def remove(self):
        if self.isEmpty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class ExploredSet():
        
        def __init__(self):
            self.set = []

        def add(self, node):
            self.set.append(node)

        def contains_state(self, state):
            return any(node.state == state for node in self.set)
