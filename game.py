import pygame, sys, random
from entities.pokemon import Pokemon
from utils import get_pokemon, key_down, get_initials_pokemons, set_volume_for_sounds

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 640, 480
        self.janela = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Pokémon System Battle')

        selector = PokemonSelector(self.width, self.height)
        self.selected_pokemon = selector.run(self.janela)
        self.front, self.back, self.nome, self.nivel, self.life = self.selected_pokemon
        self.pokemon = Pokemon(self.nome, self.nivel, self.life)

        self.fundo = pygame.image.load("assets/background/fundo.png")
        self.menu = pygame.image.load("assets/hud/menu.png")
        self.player = pygame.image.load("assets/player/player_idle.png")
        self.option = pygame.image.load("assets/hud/bar-options.png")
        self.lifeBarBack = pygame.image.load("assets/hud/bar-life-back.png")
        self.lifeBarBack2 = pygame.image.load("assets/hud/bar-life-back.png")
        self.cursor = pygame.image.load("assets/others/cursor.png")
        self.lifeBar = pygame.image.load("assets/hud/bar-life.png")
        self.enemy, self.enemy_back, self.enemy_nome, self.enemy_nivel, self.enemy_life = get_pokemon(self.width, self.height)
                
        self.fundo = pygame.transform.scale(self.fundo, (self.width, 340))
        self.player = pygame.transform.scale(self.player, (self.width // 2, self.height // 3))
        self.menu = pygame.transform.scale(self.menu, (self.width, 140))
        self.option = pygame.transform.scale(self.option, (self.width // 2, 140))
        self.lifeBarBack = pygame.transform.scale(self.lifeBarBack, (self.width // 2, self.height // 6))
        self.lifeBarBack2 = pygame.transform.scale(self.lifeBarBack2, (self.width // 2, self.height // 6))
        self.enemy = pygame.transform.scale(self.enemy, (self.width // 5, self.height // 4))
        self.cursor = pygame.transform.scale(self.cursor, (self.width // 25, self.height // 20))
        self.selected_sprite = pygame.transform.scale(self.front, (self.width // 5, self.height // 4))

        self.cursor_x, self.cursor_y = 335, 380
        
        pygame.mixer.music.load("musics/Battle!.mp3")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(True)
        
        self.sf_teclas = pygame.mixer.Sound("musics/effects/menu/select.wav")
        self.sf_teclas.set_volume(.7)

        self.sf_attack1 = pygame.mixer.Sound("musics/effects/battle/firered_000C.wav")
        self.sf_attack2 = pygame.mixer.Sound("musics/effects/battle/firered_000D.wav")

        self.enter_pressed = False
        self.key_pressed = False

    def run(self):
        while True:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if events.type == pygame.KEYDOWN and not self.key_pressed:
                self.key_pressed = True
                if events.key == pygame.K_UP:
                    self.sf_teclas.play()
                    self.cursor_y = 380
                elif events.key == pygame.K_DOWN:
                    self.sf_teclas.play()
                    self.cursor_y = 425
                elif events.key == pygame.K_LEFT:
                    self.sf_teclas.play()
                    self.cursor_x = 335
                elif events.key == pygame.K_RIGHT:
                    self.sf_teclas.play()
                    self.cursor_x = 485
                elif events.key == pygame.K_RETURN:
                    if self.cursor_y == 380 and self.cursor_x == 335:
                        random.choice([self.sf_attack1, self.sf_attack2]).play()
                        self.pokemon.takeDamage(1)
                    elif self.cursor_y == 380 and self.cursor_x == 485:
                        print('mochila')
                    elif self.cursor_y == 425 and self.cursor_x == 335:
                        print('pokemon')
                    elif self.cursor_y == 425 and self.cursor_x == 485:
                        print('fugir')

            if events.type == pygame.KEYUP:
                self.key_pressed = False

            self.janela.blit(self.fundo, (0, 0))
            self.janela.blit(self.menu, (0, 340))
            self.janela.blit(self.option, (320, 340))
            self.janela.blit(self.lifeBarBack, (20, 20))
            self.janela.blit(self.lifeBarBack2, (315, 250))

            max_life_width = self.width // 2 - 162
            current_life_width = int((self.pokemon.get_life() / self.pokemon.get_maxLife()) * max_life_width)
            self.lifeBar = pygame.transform.scale(pygame.image.load("assets/hud/bar-life.png"), (current_life_width, self.height // 38))
            self.janela.blit(self.lifeBar, (142, 65))

            fonte = pygame.font.Font('fonts/pokemon_fire_red.ttf', 38)

            enemy_nome_texto = fonte.render(f"{self.enemy_nome}", True, (54, 54, 54))
            enemy_nivel_texto = fonte.render(f"{self.enemy_nivel}", True, (54, 54, 54))
            self.janela.blit(enemy_nome_texto, (40, 25))
            self.janela.blit(enemy_nivel_texto, (285, 25))
            self.janela.blit(self.enemy, (400, 80))

            jogador_nome_texto = fonte.render(f"{self.nome}", True, (54, 54, 54))
            jogador_nivel_texto = fonte.render(f"{self.nivel}", True, (54, 54, 54))
            self.janela.blit(jogador_nome_texto, (350, 255))
            self.janela.blit(jogador_nivel_texto, (580, 255))
            self.janela.blit(self.back, (80, 200))

            self.janela.blit(self.cursor, (self.cursor_x, self.cursor_y))
            pygame.display.flip()

class PokemonSelector:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pokemons = get_initials_pokemons(width, height)
        self.pokemon_selected = 0
        self.key_pressed = False

        self.fundo = pygame.image.load("assets/Background/menu.png")
        self.title = pygame.image.load("assets/others/title.png")
        self.credits = pygame.image.load("assets/others/credits.png")
        self.pokeball = pygame.image.load("assets/others/pokeball.png")
        self.pokeball_x = 80

        self.text_font = pygame.font.Font('fonts/pokemon_fire_red.ttf', 38)

        pygame.mixer.music.load("musics/1-20. Pokémon Gym.mp3")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(True)
        
        self.sf_key = pygame.mixer.Sound("musics/effects/menu/select.wav")
        self.sf_key_selected = pygame.mixer.Sound("musics/effects/menu/selected.wav")
        self.sf_key_selected.set_volume(1)

        sounds = [self.sf_key]
        set_volume_for_sounds(sounds, .1)
    
    def run(self, window):
        while True:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if events.type == pygame.KEYDOWN and not self.key_pressed:
                self.key_pressed = True
                if events.key == pygame.K_LEFT:
                    self.pokemon_selected = (self.pokemon_selected - 1) % 3
                    self.sf_key.play()
                    self.pokeball_x -= 160

                elif events.key == pygame.K_RIGHT:
                    self.pokemon_selected = (self.pokemon_selected + 1) % 3
                    self.sf_key.play()
                    self.pokeball_x += 160

                elif events.key == pygame.K_RETURN:
                    self.sf_key_selected.play()
                    return self.pokemons[self.pokemon_selected]
            
            if self.pokeball_x > 400: self.pokeball_x = 80
            elif self.pokeball_x < 80: self.pokeball_x = 400

            if events.type == pygame.KEYUP:
                self.key_pressed = False
                
            window.blit(self.fundo, (0, 0))
            window.blit(self.title, (100, 60))
            window.blit(self.credits, (300, 120))

            for index, (front, back, name, level, life) in enumerate(self.pokemons):
                x = (self.width // 4) * (index + 1) - (front.get_width() // 2) #80, 240, 400
                y = self.height // 2 + 30                                       #320
                window.blit(front, (x, y))

                name_text = self.text_font.render(name, True, (255, 255, 255))
                window.blit(name_text, (x + 32, y + front.get_height() + 20))

            window.blit(self.pokeball, (self.pokeball_x, 320))

            pygame.display.flip()

# ---