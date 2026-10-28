
import pygame
import random

# Configurar o áudio antes de inicializar o Pygame
pygame.mixer.pre_init(
    frequency=44100,
    size=-16,
    channels=2,
    buffer=512
)

pygame.init()

LARGURA = 800
ALTURA = 600
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cyber-Grid")

relogio = pygame.time.Clock()

from jogador import Jogador
from tiro import Tiro
from inimigo import InimigoZigueZague
from explosao import Explosao

# Fontes
fonte_titulo = pygame.font.SysFont("arial", 60, bold=True)
fonte = pygame.font.SysFont("arial", 30)
fonte_menor = pygame.font.SysFont("arial", 20)

# Cores dos textos: preto
BRANCO = (255, 255, 255)
AZUL = (0, 150, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Carregar o som uma única vez
som_morte = pygame.mixer.Sound(
    "sons/inimigo_morre.mp3"
)
som_morte.set_volume(0.5)

# Reservar canais para os efeitos sonoros
pygame.mixer.set_num_channels(16)
canal_morte = pygame.mixer.Channel(1)

# Carregar fundo
try:
    fundo = pygame.image.load(
        "imagens/fundo.png"
    ).convert()

    fundo = pygame.transform.scale(
        fundo, (LARGURA, ALTURA)
    )
except pygame.error:
    fundo = None


def desenhar_texto(texto, fonte_usada, cor, y):
    imagem = fonte_usada.render(
        texto, True, cor
    )

    retangulo = imagem.get_rect(
        center=(LARGURA // 2, y)
    )

    tela.blit(imagem, retangulo)


def desenhar_fundo():
    if fundo:
        tela.blit(fundo, (0, 0))
    else:
        tela.fill((15, 20, 35))


def menu_inicial():
    while True:
        relogio.tick(FPS)
        desenhar_fundo()

        desenhar_texto(
            "CYBER-GRID", fonte_titulo, AZUL, 180
        )
        desenhar_texto(
            "Defenda a galáxia!", fonte, BRANCO, 250
        )
        desenhar_texto(
            "ENTER - Jogar", fonte, VERDE, 350
        )
        desenhar_texto(
            "ESC - Sair", fonte_menor, BRANCO, 410
        )

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return True

                if evento.key == pygame.K_ESCAPE:
                    return False


def tela_game_over(pontos):
    while True:
        relogio.tick(FPS)
        desenhar_fundo()

        desenhar_texto(
            "FIM DE JOGO", fonte_titulo, VERMELHO, 180
        )
        desenhar_texto(
            f"Pontuação: {pontos}", fonte, BRANCO, 270
        )
        desenhar_texto(
            "R - Jogar novamente", fonte, VERDE, 350
        )
        desenhar_texto(
            "M - Voltar ao menu", fonte, AZUL, 400
        )
        desenhar_texto(
            "ESC - Sair", fonte_menor, BRANCO, 450
        )

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return "jogar"

                if evento.key == pygame.K_m:
                    return "menu"

                if evento.key == pygame.K_ESCAPE:
                    return "sair"


def jogar():
    todos_sprites = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    tiros = pygame.sprite.Group()

    jogador = Jogador(
        LARGURA // 2,
        ALTURA - 70
    )

    todos_sprites.add(jogador)

    pontos = 0
    spawn_timer = 0

    while True:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "menu"

                if evento.key == pygame.K_SPACE:
                    tiro = Tiro(
                        jogador.rect.centerx,
                        jogador.rect.top
                    )

                    todos_sprites.add(tiro)
                    tiros.add(tiro)

        # Criar inimigos
        spawn_timer += 1

        if spawn_timer >= 40:
            inimigo = InimigoZigueZague(
                random.randint(30, LARGURA - 30),
                -40
            )

            todos_sprites.add(inimigo)
            inimigos.add(inimigo)
            spawn_timer = 0

        # Colisão entre tiros e inimigos
        colisoes = pygame.sprite.groupcollide(
            tiros,
            inimigos,
            True,
            True
        )

        for inimigos_atingidos in colisoes.values():
            for inimigo in inimigos_atingidos:

                # Tocar o som sem esperar terminar outro efeito
                canal_morte.play(som_morte)

                explosao = Explosao(
                    inimigo.rect.centerx,
                    inimigo.rect.centery
                )

                todos_sprites.add(explosao)
                pontos += 1

        # Colisão entre jogador e inimigos
        atingidos = pygame.sprite.spritecollide(
            jogador,
            inimigos,
            True
        )

        if atingidos:
            jogador.vida -= len(atingidos)

        # Atualizar objetos
        todos_sprites.update()

        # Desenhar jogo
        desenhar_fundo()
        todos_sprites.draw(tela)

        texto_status = fonte_menor.render(
            f"Vida: {max(0, jogador.vida)}"
            f" | Pontos: {pontos}"
            f" | ESC: Menu",
            True,
            BRANCO
        )

        tela.blit(texto_status, (15, 15))
        pygame.display.flip()

        # Mostrar fim de jogo sem fechar a janela
        if jogador.vida <= 0:
            return tela_game_over(pontos)


# Loop principal
aberto = True

while aberto:
    if not menu_inicial():
        break

    resultado = jogar()

    while resultado == "jogar":
        resultado = jogar()

    if resultado == "sair":
        aberto = False

pygame.quit()
