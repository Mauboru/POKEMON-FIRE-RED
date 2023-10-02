import pygame
import sys

pygame.init()

# Configurações da janela
largura, altura = 640, 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Pokémon Battle')

# Carregue as imagens para o fundo e outros elementos
fundo = pygame.image.load("sprites/fundo.png")
menu = pygame.image.load("sprites/menu.png")
player = pygame.image.load("sprites/player_idle.png")
option = pygame.image.load("sprites/bar-options.png")
life = pygame.image.load("sprites/bar-life.png")
cursor = pygame.image.load("sprites/cursor.png")
enemy = pygame.image.load("sprites/enemy.png")

# Redimensione as imagens para preencher a tela mantendo a proporção
fundo = pygame.transform.scale(fundo, (largura, 340))
player = pygame.transform.scale(player, (largura//2, altura//3))
menu = pygame.transform.scale(menu, (largura, 140))
option = pygame.transform.scale(option, (largura//2, 140))
life = pygame.transform.scale(life, (largura//2, altura//6))
enemy = pygame.transform.scale(enemy, (largura//5, altura//4))
cursor = pygame.transform.scale(cursor, (largura//25, altura//20))

# Posição inicial do cursor
cursor_x, cursor_y = 335, 380

# Carregando a música de fundo
pygame.mixer.music.load("musics/Battle!.mp3")
pygame.mixer.music.play(True)
pygame.mixer.music.set_volume(.5)

# Loop principal do jogo
rodando = True
cima = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # Controle de teclado para mover o cursor
        if evento.type == pygame.KEYDOWN:
            #troca posicao
            if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN :
                cima = not cima
                pygame.mixer.music.load("musics/firered_00A0.wav")
                pygame.mixer.music.play(False)
                pygame.mixer.music.set_volume(.5)
            if cima:
                cursor_y = 380
            elif not cima:
                cursor_y = 425
            if evento.key == pygame.K_LEFT:
                cursor_x = 335
                pygame.mixer.music.load("musics/firered_00A0.wav")
                pygame.mixer.music.play(False)
                pygame.mixer.music.set_volume(.5)
            elif evento.key == pygame.K_RIGHT:
                cursor_x = 485
                pygame.mixer.music.load("musics/firered_00A0.wav")
                pygame.mixer.music.play(False)
                pygame.mixer.music.set_volume(.5)
    print(cima, cursor_x, cursor_y)

    # Atualize a lógica do jogo aqui

    # Desenhe os elementos na tela
    tela.blit(fundo, (0, 0))
    tela.blit(player, (120, 180))
    tela.blit(menu, (0, 340))
    tela.blit(option, (320, 340))
    tela.blit(life, (20, 20))
    tela.blit(enemy, (400, 80))
    tela.blit(cursor, (cursor_x, cursor_y))
    pygame.display.flip()

# Encerre o Pygame
pygame.quit()
sys.exit()