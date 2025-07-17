class No:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def altura(self, no):
        if not no:
            return 0
        return no.altura

    def balanceamento(self, no):
        if not no:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def inserir(self, raiz, valor):
        if not raiz:
            return No(valor)
        elif valor < raiz.valor:
            raiz.esquerda = self.inserir(raiz.esquerda, valor)
        else:
            raiz.direita = self.inserir(raiz.direita, valor)

        raiz.altura = 1 + max(self.altura(raiz.esquerda), self.altura(raiz.direita))
        balance = self.balanceamento(raiz)

        # Rotação à direita
        if balance > 1 and valor < raiz.esquerda.valor:
            return self.rotacionar_direita(raiz)

        # Rotação à esquerda
        if balance < -1 and valor > raiz.direita.valor:
            return self.rotacionar_esquerda(raiz)

        # Rotação esquerda-direita
        if balance > 1 and valor > raiz.esquerda.valor:
            raiz.esquerda = self.rotacionar_esquerda(raiz.esquerda)
            return self.rotacionar_direita(raiz)

        # Rotação direita-esquerda
        if balance < -1 and valor < raiz.direita.valor:
            raiz.direita = self.rotacionar_direita(raiz.direita)
            return self.rotacionar_esquerda(raiz)

        return raiz

    def remover(self, raiz, valor):
        if not raiz:
            return raiz

        if valor < raiz.valor:
            raiz.esquerda = self.remover(raiz.esquerda, valor)
        elif valor > raiz.valor:
            raiz.direita = self.remover(raiz.direita, valor)
        else:
            if not raiz.esquerda:
                temp = raiz.direita
                raiz = None
                return temp
            elif not raiz.direita:
                temp = raiz.esquerda
                raiz = None
                return temp

            temp = self.minimo_valor_no(raiz.direita)
            raiz.valor = temp.valor
            raiz.direita = self.remover(raiz.direita, temp.valor)

        if not raiz:
            return raiz

        raiz.altura = 1 + max(self.altura(raiz.esquerda), self.altura(raiz.direita))
        balance = self.balanceamento(raiz)

        # Rotação à direita
        if balance > 1 and self.balanceamento(raiz.esquerda) >= 0:
            return self.rotacionar_direita(raiz)

        # Rotação à esquerda
        if balance < -1 and self.balanceamento(raiz.direita) <= 0:
            return self.rotacionar_esquerda(raiz)

        # Rotação esquerda-direita
        if balance > 1 and self.balanceamento(raiz.esquerda) < 0:
            raiz.esquerda = self.rotacionar_esquerda(raiz.esquerda)
            return self.rotacionar_direita(raiz)

        # Rotação direita-esquerda
        if balance < -1 and self.balanceamento(raiz.direita) > 0:
            raiz.direita = self.rotacionar_direita(raiz.direita)
            return self.rotacionar_esquerda(raiz)

        return raiz

    def rotacionar_esquerda(self, z):
        y = z.direita
        T2 = y.esquerda

        y.esquerda = z
        z.direita = T2

        z.altura = 1 + max(self.altura(z.esquerda), self.altura(z.direita))
        y.altura = 1 + max(self.altura(y.esquerda), self.altura(y.direita))

        return y

    def rotacionar_direita(self, z):
        y = z.esquerda
        T3 = y.direita

        y.direita = z
        z.esquerda = T3

        z.altura = 1 + max(self.altura(z.esquerda), self.altura(z.direita))
        y.altura = 1 + max(self.altura(y.esquerda), self.altura(y.direita))

        return y

    def minimo_valor_no(self, raiz):
        atual = raiz
        while atual.esquerda:
            atual = atual.esquerda
        return atual

    def buscar(self, raiz, valor):
        if not raiz or raiz.valor == valor:
            return raiz
        if valor < raiz.valor:
            return self.buscar(raiz.esquerda, valor)
        return self.buscar(raiz.direita, valor)

    def inserir_valor(self, valor):
        self.raiz = self.inserir(self.raiz, valor)

    def remover_valor(self, valor):
        self.raiz = self.remover(self.raiz, valor)

    def buscar_valor(self, valor):
        return self.buscar(self.raiz, valor)


# Exemplo de uso:
if __name__ == "__main__":
    arvore = ArvoreAVL()
    arvore.inserir_valor(10)
    arvore.inserir_valor(20)
    arvore.inserir_valor(30)
    arvore.inserir_valor(40)
    arvore.inserir_valor(50)

    print("Árvore após inserções:")
    def percurso_em_ordem(raiz):
        if raiz:
            percurso_em_ordem(raiz.esquerda)
            print(raiz.valor)
            percurso_em_ordem(raiz.direita)

    percurso_em_ordem(arvore.raiz)
    print()

    arvore.remover_valor(20)