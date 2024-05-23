import pygame, sys, requests, random, io
from entities.pokemon import Pokemon

pygame.init()

#Funções
def get_pokemon():
    try:
        numero = random.randint(1, 898)
        api = f"https://pokeapi.co/api/v2/pokemon/{numero}/"
        response = requests.get(api)
        dados = response.json()

        #Info do pokemon
        sprite_url = dados['sprites']['versions']['generation-v']['black-white']['animated']['front_default']
        nome = dados['name']
        nivel = random.randint(1,10)

        response_imagem = requests.get(sprite_url)
        imagem_bytes = io.BytesIO(response_imagem.content)
        sprite = pygame.image.load(imagem_bytes)
        sprite = pygame.transform.scale(sprite, (largura//4, altura//4))
        return sprite, nome, nivel
    except Exception as e:
        print(f"Erro ao carregar o sprite: {e}")
        return get_pokemon()

def key_down(key):
    if evento.type == pygame.KEYDOWN:
        if evento.key == key:
            return True
        else:
            return False

# Configurações da janela
largura, altura = 640, 480
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Pokémon Battle')

# Carregue as imagens para o fundo e outros elementos
fundo = pygame.image.load("assets/Background/fundo.png")
menu = pygame.image.load("assets/HUD/menu.png")
player = pygame.image.load("assets/Player/player_idle.png")
option = pygame.image.load("assets/HUD/bar-options.png")
bar_life = pygame.image.load("assets/HUD/bar-life-back.png")
life = pygame.image.load("assets/HUD/bar-life.png")
cursor = pygame.image.load("assets/Outros/cursor.png")
enemy, nome, nivel = get_pokemon()

#Iniciando o inimigo
pokemon = Pokemon(nome, nivel, 10)

# Redimensionando as imagens
fundo = pygame.transform.scale(fundo, (largura, 340))
player = pygame.transform.scale(player, (largura//2, altura//3))
menu = pygame.transform.scale(menu, (largura, 140))
option = pygame.transform.scale(option, (largura//2, 140))
bar_life = pygame.transform.scale(bar_life, (largura//2, altura//6))
enemy = pygame.transform.scale(enemy, (largura//5, altura//4))
cursor = pygame.transform.scale(cursor, (largura//25, altura//20))

# Posição inicial do cursor
cursor_x, cursor_y = 335, 380

# Carregando a música de fundo
pygame.mixer.music.load("musics/Battle!.mp3")
pygame.mixer.music.set_volume(.1)
pygame.mixer.music.play(True)

# Efeito sonoro para as setas
sf_teclas = pygame.mixer.Sound("musics/firered_00A0.wav")
sf_teclas.set_volume(.7)

# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # Controle de teclado para mover o cursor
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP :
                sf_teclas.play()
                cursor_y = 380
            elif evento.key == pygame.K_DOWN:
                sf_teclas.play()
                cursor_y = 425
            elif evento.key == pygame.K_LEFT:
                sf_teclas.play()
                cursor_x = 335
            elif evento.key == pygame.K_RIGHT:
                sf_teclas.play()
                cursor_x = 485

    # Atualize a lógica do jogo aqui
    if cursor_y == 380 and cursor_x == 335:
        if key_down(pygame.K_RETURN):
            #fazer algo
            print()
    elif cursor_y == 380 and cursor_x == 485:
        print('mochila')
    elif cursor_y == 425 and cursor_x == 335:
        print('pokemon')
    elif cursor_y == 425 and cursor_x == 485:
        print('fugir')

    # Desenhe os elementos na janela
    janela.blit(fundo, (0, 0))
    janela.blit(player, (60, 180))
    janela.blit(menu, (0, 340))
    janela.blit(option, (320, 340))
    janela.blit(bar_life, (20, 20))
    
    # Desenha o nome e o nível na tela
    fonte = pygame.font.Font('fonts/pokemon_fire_red.ttf', 38)
    nome_texto = fonte.render(f"{nome}", True, (54, 54, 54))
    nivel_texto = fonte.render(f"{nivel}", True, (54, 54, 54))
    janela.blit(nome_texto, (40, 25))
    janela.blit(nivel_texto, (285, 25))
    
    janela.blit(enemy, (400, 80))
    janela.blit(cursor, (cursor_x, cursor_y))
    pygame.display.flip()

# Encerre o Pygame
pygame.quit()
sys.exit()