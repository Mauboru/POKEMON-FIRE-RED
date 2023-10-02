import pygame
import sys

pygame.init()

# Configurações da janela
largura, altura = 640, 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Pokémon Battle')

# Carregue as imagens para o fundo e outros elemento
fundo = pygame.image.load("sprites/fundo.png")
menu = pygame.image.load("sprites/menu.png")
player = pygame.image.load("sprites/player_idle.png")
option = pygame.image.load("sprites/bar-options.png")
life = pygame.image.load("sprites/bar-life.png")
cursor = pygame.image.load("sprites/cursor.png")
enemy = pygame.image.load("sprites/enemy.png")

# Redimensione as imagens para preencher a tela mantendo a proporção
fundo = pygame.transform.scale(fundo, (largura, 340))
player = pygame.transform.scale(player, (largura/2.5, altura/3))
menu = pygame.transform.scale(menu, (largura, 140))
option = pygame.transform.scale(option, (largura/2, 140))
life = pygame.transform.scale(life, (largura/2, altura/6))
enemy = pygame.transform.scale(enemy, (largura/5, altura/4))

# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Atualize a lógica do jogo aqui

    # Desenhe os elementos na tela
    tela.blit(fundo, (0, 0))
    tela.blit(player, (120, 180))
    tela.blit(menu, (0, 340))
    tela.blit(option, (320, 340))
    tela.blit(life, (20, 20))
    tela.blit(enemy, (400, 80))
    pygame.display.flip()

# Encerre o Pygame
pygame.quit()
sys.exit()