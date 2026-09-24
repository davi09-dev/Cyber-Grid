import pygame
from entidade import Entidade


class Tiro(Entidade):

    def __init__(self, x, y):
        super().__init__(x, y, 10)

        self.image = pygame.Surface((6, 20))
        self.image.fill((255, 255, 0))

        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self):

        self.rect.y -= self.velocidade

        if self.rect.bottom < 0:
            self.kill()