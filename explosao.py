
import pygame


class Explosao(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        imagem = pygame.image.load(
            "imagens/explosao.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            imagem,
            (54, 54)
        )

        self.rect = self.image.get_rect(
            center=(x, y)
        )

        self.tempo = 12

    def update(self):

        self.tempo -= 1

        if self.tempo <= 0:
            self.kill()
