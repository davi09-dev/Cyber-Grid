
import pygame
from entidade import Entidade


class Tiro(Entidade):

    def __init__(self, x, y):
        super().__init__(x, y, 10)

        imagem = pygame.image.load(
            "imagens/tiro.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            imagem,
            (36, 12)
        )

        # Os projéteis originais estão na horizontal.
        # Giramos para apontar para cima.
        self.image = pygame.transform.rotate(
            self.image,
            90
        )

        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self):

        self.rect.y -= self.velocidade

        if self.rect.bottom < 0:
            self.kill()
