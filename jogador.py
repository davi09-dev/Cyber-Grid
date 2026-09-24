import pygame
from entidade import Entidade


class Jogador(Entidade):

    def __init__(self, x, y):
        super().__init__(x, y, 6)

        self.image.fill((0, 150, 255))
        self.vida = 5

    def update(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.mover(0, -self.velocidade)

        if keys[pygame.K_s]:
            self.mover(0, self.velocidade)

        if keys[pygame.K_a]:
            self.mover(-self.velocidade, 0)

        if keys[pygame.K_d]:
            self.mover(self.velocidade, 0)

        # Limites da tela
        self.rect.x = max(0, min(self.rect.x, 800 - 40))
        self.rect.y = max(0, min(self.rect.y, 600 - 40))