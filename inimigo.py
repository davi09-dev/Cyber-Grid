
import pygame
import random
from entidade import Entidade


class Inimigo(Entidade):

    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)

        imagens = [
            "imagens/inimigo1.png",
            "imagens/inimigo2.png",
            "imagens/inimigo3.png"
        ]

        caminho = random.choice(imagens)

        imagem = pygame.image.load(
            caminho
        ).convert_alpha()

        self.image = pygame.transform.scale(
            imagem,
            (80, 80)
        )

        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def atualizar_posicao(self):
        raise NotImplementedError


class InimigoZigueZague(Inimigo):

    def __init__(self, x, y):
        super().__init__(x, y, 3)

        self.direcao = 1

    def atualizar_posicao(self):

        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3

        if self.rect.left <= 0:
            self.direcao = 1

        if self.rect.right >= 800:
            self.direcao = -1

    def update(self):

        self.atualizar_posicao()

        if self.rect.top > 600:
            self.kill()
