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
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.pokemons = get_initials_pokemons(largura, altura)
        self.selected = 0
        self.last_key_press_time = 0
        self.key_cooldown = 200 
    
    def run(self, janela):
        rodando = True
        while rodando:
            current_time = pygame.time.get_ticks()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if evento.type == pygame.KEYDOWN and (current_time - self.last_key_press_time > self.key_cooldown):
                self.last_key_press_time = current_time
                if evento.key == pygame.K_LEFT:
                    self.selected = (self.selected - 1) % 3
                elif evento.key == pygame.K_RIGHT:
                    self.selected = (self.selected + 1) % 3
                elif evento.key == pygame.K_RETURN:
                    return self.pokemons[self.selected]
                
            janela.fill((255, 255, 255))
            fonte = pygame.font.Font('fonts/pokemon_fire_red.ttf', 36)

            for index, (sprite, nome, nivel, life) in enumerate(self.pokemons):
                x = self.largura // 4 * (index + 1) - sprite.get_width() // 2
                y = self.altura // 2 - sprite.get_height() // 2
                janela.blit(sprite, (x, y))
                if index == self.selected:
                    pygame.draw.rect(janela, (255, 0, 0), (x - 5, y - 5, sprite.get_width() + 10, sprite.get_height() + 10), 3)
                nome_texto = fonte.render(nome, True, (0, 0, 0))
                janela.blit(nome_texto, (x, y + sprite.get_height() + 10))

            pygame.display.flip()

# proxima classe