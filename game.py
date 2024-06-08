import pygame, sys, random
from entities.pokemon import Pokemon
from utils import get_pokemon, key_down, get_initials_pokemons

class Game:
    def __init__(self):
        pygame.init()
        self.largura, self.altura = 640, 480
        self.janela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Pokémon Battle')

        # Carregando tela de selecao de pokemon
        selector = PokemonSelector(self.largura, self.altura)
        self.selected_pokemon = selector.run(self.janela)
        self.selected_sprite, self.nome, self.nivel, self.life = self.selected_pokemon

        # Carregando as imagens
        self.fundo = pygame.image.load("assets/Background/fundo.png")
        self.menu = pygame.image.load("assets/HUD/menu.png")
        self.player = pygame.image.load("assets/Player/player_idle.png")
        self.option = pygame.image.load("assets/HUD/bar-options.png")
        self.lifeBarBack = pygame.image.load("assets/HUD/bar-life-back.png")
        self.cursor = pygame.image.load("assets/Outros/cursor.png")
        self.lifeBar = pygame.image.load("assets/HUD/bar-life.png")
        self.enemy, self.nome, self.nivel, self.life = get_pokemon(self.largura, self.altura)
    
        # Iniciando o inimigo
        self.pokemon = Pokemon(self.nome, self.nivel, self.life)
        
        # Redimensionando as imagens
        self.fundo = pygame.transform.scale(self.fundo, (self.largura, 340))
        self.player = pygame.transform.scale(self.player, (self.largura // 2, self.altura // 3))
        self.menu = pygame.transform.scale(self.menu, (self.largura, 140))
        self.option = pygame.transform.scale(self.option, (self.largura // 2, 140))
        self.lifeBarBack = pygame.transform.scale(self.lifeBarBack, (self.largura // 2, self.altura // 6))
        self.enemy = pygame.transform.scale(self.enemy, (self.largura // 5, self.altura // 4))
        self.cursor = pygame.transform.scale(self.cursor, (self.largura // 25, self.altura // 20))
        self.selected_sprite = pygame.transform.scale(self.selected_sprite, (self.largura // 5, self.altura // 4))

        # Posição inicial do cursor
        self.cursor_x, self.cursor_y = 335, 380
        
        # Carregando a música de fundo
        pygame.mixer.music.load("musics/Battle!.mp3")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(True)
        
        # Efeito sonoro para as setas
        self.sf_teclas = pygame.mixer.Sound("musics/effects/menu/firered_00A0.wav")
        self.sf_teclas.set_volume(.7)

        self.sfAttack1 = pygame.mixer.Sound("musics/effects/battle/firered_000C.wav")
        self.sfAttack2 = pygame.mixer.Sound("musics/effects/battle/firered_000D.wav")

        self.enter_pressed = False

    def run(self):
        rodando = True
        start_time = pygame.time.get_ticks()
        while rodando:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time

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
                    elif evento.key == pygame.K_RETURN:
                        self.enter_pressed = True

                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_RETURN:
                        self.enter_pressed = False

            # Lógica do jogo
            if self.cursor_y == 380 and self.cursor_x == 335:
                if self.enter_pressed:
                    self.pokemon.takeDamage(1)
                    random.choice([self.sfAttack1, self.sfAttack2]).play()
                    self.enter_pressed = False

            elif self.cursor_y == 380 and self.cursor_x == 485:
                print('mochila')
            elif self.cursor_y == 425 and self.cursor_x == 335:
                print('pokemon')
            elif self.cursor_y == 425 and self.cursor_x == 485:
                print('fugir')

            # Desenhe os elementos na janela
            self.janela.blit(self.fundo, (0, 0))
            if elapsed_time < 3000:
                self.janela.blit(self.player, (60, 180))
            else:
                self.janela.blit(self.selected_sprite, (60, 180))

            self.janela.blit(self.menu, (0, 340))
            self.janela.blit(self.option, (320, 340))
            self.janela.blit(self.lifeBarBack, (20, 20))

            # Calcular a largura da barra de vida
            max_life_width = self.largura // 2 - 162
            current_life_width = int((self.pokemon.get_life() / self.pokemon.get_maxLife()) * max_life_width)
            self.lifeBar = pygame.transform.scale(pygame.image.load("assets/HUD/bar-life.png"), (current_life_width, self.altura // 38))
            self.janela.blit(self.lifeBar, (142, 65))

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

class PokemonSelector:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pokemons = get_initials_pokemons(width, height)
        self.pokemon_selected = 0

        # pygame.mixer.music.load("musics/Battle!.mp3")
        # pygame.mixer.music.set_volume(.1)
        # pygame.mixer.music.play(True)
        
        self.sf_teclas = pygame.mixer.Sound("musics/effects/menu/firered_00A0.wav")
        self.sf_teclas.set_volume(.7)
    
    def run(self, window):
        while True:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_LEFT:
                    self.pokemon_selected = (self.pokemon_selected - 1) % 3
                    self.sf_teclas.play()
                elif events.key == pygame.K_RIGHT:
                    self.pokemon_selected = (self.pokemon_selected + 1) % 3
                    self.sf_teclas.play()
                elif events.key == pygame.K_RETURN:
                    # adicionar som de confirmacao
                    return self.pokemons[self.pokemon_selected]
                
            window.fill((255, 255, 255)) # adicionar imagem de fundo
            fonts = pygame.font.Font('fonts/pokemon_fire_red.ttf', 38)

            for index, (sprite, name, level, life) in enumerate(self.pokemons):
                x = (self.width // 4) * (index + 1) - (sprite.get_width() // 2) #80, 240, 400
                y = self.height // 2.7                                          #177
                window.blit(sprite, (x, y))

                if index == self.pokemon_selected:
                    # desenhar o quadrado seletor
                    pygame.draw.rect(window, (255, 0, 0), (x - 5, y - 5, sprite.get_width() + 10, sprite.get_height() + 10), 3)
                name_text = fonts.render(name, True, (0, 0, 0))
                window.blit(name_text, (x + 32, y + sprite.get_height() + 20))

            pygame.display.flip()

# ---