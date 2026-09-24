import pygame
import random

from jogador import Jogador
from tiro import Tiro
from inimigo import InimigoZigueZague


pygame.init()


# CONFIGURAÇÕES

LARGURA = 800
ALTURA = 600

TELA = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption("Nave Espacial")

FPS = 60
clock = pygame.time.Clock()


# GRUPOS

todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()


# JOGADOR

jogador = Jogador(
    LARGURA // 2,
    ALTURA - 60
)

todos_sprites.add(jogador)


# VARIÁVEIS

pontos = 0
spawn_timer = 0


# LOOP DO JOGO

rodando = True

while rodando:

    clock.tick(FPS)

    # EVENTOS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                tiro = Tiro(
                    jogador.rect.centerx,
                    jogador.rect.top
                )

                todos_sprites.add(tiro)
                tiros.add(tiro)


    # CRIAR INIMIGOS

    spawn_timer += 1

    if spawn_timer > 40:

        inimigo = InimigoZigueZague(
            random.randint(40, LARGURA - 40),
            -40
        )

        todos_sprites.add(inimigo)
        inimigos.add(inimigo)

        spawn_timer = 0


    # COLISÃO TIRO X INIMIGO

    colisao = pygame.sprite.groupcollide(
        inimigos,
        tiros,
        True,
        True
    )

    pontos += len(colisao)


    # COLISÃO INIMIGO X JOGADOR

    if pygame.sprite.spritecollide(
        jogador,
        inimigos,
        True
    ):

        jogador.vida -= 1

        if jogador.vida <= 0:

            print("GAME OVER!")
            rodando = False


    # ATUALIZAR

    todos_sprites.update()


    # DESENHAR

    TELA.fill((10, 10, 30))

    todos_sprites.draw(TELA)


    # PAINEL

    font = pygame.font.SysFont(
        None,
        30
    )

    texto = font.render(
        f"Vida: {jogador.vida} | Pontos: {pontos}",
        True,
        (255, 255, 255)
    )

    TELA.blit(
        texto,
        (10, 10)
    )


    pygame.display.flip()


pygame.quit()