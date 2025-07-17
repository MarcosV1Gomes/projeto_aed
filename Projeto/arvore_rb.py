# Classe que representa um nó da Árvore Rubro-Negra
class NoRB:
    def __init__(self, valor, cor='vermelho'):
        self.valor = valor
        self.cor = cor
        self.esquerda = None
        self.direita = None
        self.pai = None

    # Retorna o avô do nó
    def avo(self):
        if self.pai is None:
            return None
        return self.pai.pai

    # Retorna o irmão do nó
    def irmao(self):
        if self.pai is None:
            return None
        if self == self.pai.esquerda:
            return self.pai.direita
        return self.pai.esquerda

    # Retorna o tio do nó
    def tio(self):
        if self.pai is None:
            return None
        return self.pai.irmao()

# Classe que representa a Árvore Rubro-Negra
class ArvoreRubroNegra:
    def __init__(self):
        self.raiz = None

    # Busca um valor na árvore
    def buscar(self, valor):
        atual = self.raiz
        while atual is not None:
            if valor == atual.valor:
                return atual
            elif valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    # Insere um valor na árvore
    def inserir(self, valor):
        novo_no = NoRB(valor)
        if self.raiz is None:
            self.raiz = novo_no
        else:
            atual = self.raiz
            while True:
                if valor < atual.valor:
                    if atual.esquerda is None:
                        atual.esquerda = novo_no
                        novo_no.pai = atual
                        break
                    else:
                        atual = atual.esquerda
                else:
                    if atual.direita is None:
                        atual.direita = novo_no
                        novo_no.pai = atual
                        break
                    else:
                        atual = atual.direita
        self.ajustar_insercao(novo_no)

    # Corrige as propriedades após inserção
    def ajustar_insercao(self, no):
        while no.pai and no.pai.cor == 'vermelho':
            if no.pai == no.avo().esquerda:
                tio = no.tio()
                if tio and tio.cor == 'vermelho':
                    no.pai.cor = 'preto'
                    tio.cor = 'preto'
                    no.avo().cor = 'vermelho'
                    no = no.avo()
                else:
                    if no == no.pai.direita:
                        no = no.pai
                        self.rotacionar_esquerda(no)
                    no.pai.cor = 'preto'
                    no.avo().cor = 'vermelho'
                    self.rotacionar_direita(no.avo())
            else:
                tio = no.tio()
                if tio and tio.cor == 'vermelho':
                    no.pai.cor = 'preto'
                    tio.cor = 'preto'
                    no.avo().cor = 'vermelho'
                    no = no.avo()
                else:
                    if no == no.pai.esquerda:
                        no = no.pai
                        self.rotacionar_direita(no)
                    no.pai.cor = 'preto'
                    no.avo().cor = 'vermelho'
                    self.rotacionar_esquerda(no.avo())
        self.raiz.cor = 'preto'

    # Remove um valor da árvore
    def remover(self, valor):
        no_para_remover = self.buscar(valor)
        if no_para_remover is None:
            return

        if no_para_remover.esquerda is None or no_para_remover.direita is None:
            self._substituir_no(no_para_remover, no_para_remover.esquerda or no_para_remover.direita)
        else:
            sucessor = self._menor_valor(no_para_remover.direita)
            no_para_remover.valor = sucessor.valor
            self._substituir_no(sucessor, sucessor.direita)

        self.ajustar_remocao(no_para_remover)

    # Corrige as propriedades após remoção
    def ajustar_remocao(self, x):
        while x != self.raiz and x.cor == 'preto':
            if x == x.pai.esquerda:
                irmao = x.irmao()
                if irmao.cor == 'vermelho':
                    irmao.cor = 'preto'
                    x.pai.cor = 'vermelho'
                    self.rotacionar_esquerda(x.pai)
                    irmao = x.irmao()
                if (irmao.esquerda is None or irmao.esquerda.cor == 'preto') and \
                   (irmao.direita is None or irmao.direita.cor == 'preto'):
                    irmao.cor = 'vermelho'
                    x = x.pai
                else:
                    if irmao.direita is None or irmao.direita.cor == 'preto':
                        irmao.esquerda.cor = 'preto'
                        irmao.cor = 'vermelho'
                        self.rotacionar_direita(irmao)
                        irmao = x.irmao()
                    irmao.cor = x.pai.cor
                    x.pai.cor = 'preto'
                    if irmao.direita:
                        irmao.direita.cor = 'preto'
                    self.rotacionar_esquerda(x.pai)
                    x = self.raiz
            else:
                irmao = x.irmao()
                if irmao.cor == 'vermelho':
                    irmao.cor = 'preto'
                    x.pai.cor = 'vermelho'
                    self.rotacionar_direita(x.pai)
                    irmao = x.irmao()
                if (irmao.esquerda is None or irmao.esquerda.cor == 'preto') and \
                   (irmao.direita is None or irmao.direita.cor == 'preto'):
                    irmao.cor = 'vermelho'
                    x = x.pai
                else:
                    if irmao.esquerda is None or irmao.esquerda.cor == 'preto':
                        irmao.direita.cor = 'preto'
                        irmao.cor = 'vermelho'
                        self.rotacionar_esquerda(irmao)
                        irmao = x.irmao()
                    irmao.cor = x.pai.cor
                    x.pai.cor = 'preto'
                    if irmao.esquerda:
                        irmao.esquerda.cor = 'preto'
                    self.rotacionar_direita(x.pai)
                    x = self.raiz
        x.cor = 'preto'

    # Rotação à esquerda
    def rotacionar_esquerda(self, no):
        filho_direita = no.direita
        no.direita = filho_direita.esquerda

        if filho_direita.esquerda is not None:
            filho_direita.esquerda.pai = no

        filho_direita.pai = no.pai

        if no.pai is None:
            self.raiz = filho_direita
        elif no == no.pai.esquerda:
            no.pai.esquerda = filho_direita
        else:
            no.pai.direita = filho_direita

        filho_direita.esquerda = no
        no.pai = filho_direita

    # Rotação à direita
    def rotacionar_direita(self, no):
        filho_esquerda = no.esquerda
        no.esquerda = filho_esquerda.direita

        if filho_esquerda.direita is not None:
            filho_esquerda.direita.pai = no

        filho_esquerda.pai = no.pai

        if no.pai is None:
            self.raiz = filho_esquerda
        elif no == no.pai.direita:
            no.pai.direita = filho_esquerda
        else:
            no.pai.esquerda = filho_esquerda

        filho_esquerda.direita = no
        no.pai = filho_esquerda

    # Substitui um nó antigo por um novo
    def _substituir_no(self, no_antigo, novo_no):
        if no_antigo.pai is None:
            self.raiz = novo_no
        else:
            if no_antigo == no_antigo.pai.esquerda:
                no_antigo.pai.esquerda = novo_no
            else:
                no_antigo.pai.direita = novo_no
        if novo_no is not None:
            novo_no.pai = no_antigo.pai

    # Encontra o nó de menor valor em uma subárvore
    def _menor_valor(self, no):
        while no.esquerda is not None:
            no = no.esquerda
        return no

    # Percurso em-ordem (in-order)
    def percurso_em_ordem(self, no):
        if no is not None:
            self.percurso_em_ordem(no.esquerda)
            print(no.valor, end=" ")
            self.percurso_em_ordem(no.direita)


# Exemplo de uso
if __name__ == "__main__":
    arvore = ArvoreRubroNegra()
    arvore.inserir(10)
    arvore.inserir(20)
    arvore.inserir(30)
    arvore.inserir(40)
    arvore.inserir(50)
    arvore.inserir(25)

    print("Percurso em-ordem da Árvore Rubro-Negra:")
    arvore.percurso_em_ordem(arvore.raiz)
    print()

    arvore.remover(20)
    print("Percurso em-ordem após remover 20:")
    arvore.percurso_em_ordem(arvore.raiz)
    print()
