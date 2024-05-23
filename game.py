import pygame, sys
from entities.pokemon import Pokemon
from utils import get_pokemon, key_down

class Game:
    def __init__(self):
        pygame.init()
        self.largura, self.altura = 640, 480
        self.janela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Pokémon Battle')
        
        # Carregando as imagens
        self.fundo = pygame.image.load("assets/Background/fundo.png")
        self.menu = pygame.image.load("assets/HUD/menu.png")
        self.player = pygame.image.load("assets/Player/player_idle.png")
        self.option = pygame.image.load("assets/HUD/bar-options.png")
        self.bar_life = pygame.image.load("assets/HUD/bar-life-back.png")
        self.cursor = pygame.image.load("assets/Outros/cursor.png")
        self.enemy, self.nome, self.nivel, self.life = get_pokemon(self.largura, self.altura)
        
        # Iniciando o inimigo
        self.pokemon = Pokemon(self.nome, self.nivel, self.life)

        print(self.pokemon.__str__())
        
        # Redimensionando as imagens
        self.fundo = pygame.transform.scale(self.fundo, (self.largura, 340))
        self.player = pygame.transform.scale(self.player, (self.largura // 2, self.altura // 3))
        self.menu = pygame.transform.scale(self.menu, (self.largura, 140))
        self.option = pygame.transform.scale(self.option, (self.largura // 2, 140))
        self.bar_life = pygame.transform.scale(self.bar_life, (self.largura // 2, self.altura // 6))
        self.enemy = pygame.transform.scale(self.enemy, (self.largura // 5, self.altura // 4))
        self.cursor = pygame.transform.scale(self.cursor, (self.largura // 25, self.altura // 20))

        # Posição inicial do cursor
        self.cursor_x, self.cursor_y = 335, 380
        
        # Carregando a música de fundo
        pygame.mixer.music.load("musics/Battle!.mp3")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(True)
        
        # Efeito sonoro para as setas
        self.sf_teclas = pygame.mixer.Sound("musics/firered_00A0.wav")
        self.sf_teclas.set_volume(.7)

    def run(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                # Controle de teclado para mover o cursor
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        self.sf_teclas.play()
                        self.cursor_y = 380
                    elif evento.key == pygame.K_DOWN:
                        self.sf_teclas.play()
                        self.cursor_y = 425
                    elif evento.key == pygame.K_LEFT:
                        self.sf_teclas.play()
                        self.cursor_x = 335
                    elif evento.key == pygame.K_RIGHT:
                        self.sf_teclas.play()
                        self.cursor_x = 485

            # Atualize a lógica do jogo aqui
            if self.cursor_y == 380 and self.cursor_x == 335:
                if key_down(evento, pygame.K_RETURN):
                    # fazer algo
                    print()
            elif self.cursor_y == 380 and self.cursor_x == 485:
                print('mochila')
            elif self.cursor_y == 425 and self.cursor_x == 335:
                print('pokemon')
            elif self.cursor_y == 425 and self.cursor_x == 485:
                print('fugir')

            # Desenhe os elementos na janela
            self.janela.blit(self.fundo, (0, 0))
            self.janela.blit(self.player, (60, 180))
            self.janela.blit(self.menu, (0, 340))
            self.janela.blit(self.option, (320, 340))
            self.janela.blit(self.bar_life, (20, 20))
            
            # Desenha o nome e o nível na tela
            fonte = pygame.font.Font('fonts/pokemon_fire_red.ttf', 38)
            nome_texto = fonte.render(f"{self.nome}", True, (54, 54, 54))
            nivel_texto = fonte.render(f"{self.nivel}", True, (54, 54, 54))
            self.janela.blit(nome_texto, (40, 25))
            self.janela.blit(nivel_texto, (285, 25))
            
            self.janela.blit(self.enemy, (400, 80))
            self.janela.blit(self.cursor, (self.cursor_x, self.cursor_y))
            pygame.display.flip()

        pygame.quit()
        sys.exit()