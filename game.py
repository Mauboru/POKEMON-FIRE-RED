import pygame, sys, random
from entities.pokemon import Pokemon
from utils import get_pokemon, key_down, get_initials_pokemons, set_volume_for_sounds, set_damage

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 640, 480
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Pokémon System Battle')

        self.selected_pokemon = PokemonSelector(self.width, self.height).run(self.window)

        self.player_front, self.player_back, self.player_name, self.player_level, self.player_life = self.selected_pokemon
        self.enemy_front, self.enemy_back, self.enemy_name, self.enemy_level, self.enemy_life = get_pokemon(self.width, self.height)

        self.player = Pokemon(self.player_name, self.player_level, self.player_life)
        self.enemy = Pokemon(self.enemy_name, self.enemy_level, self.enemy_life)

        self.fundo = pygame.image.load("assets/background/fundo.png")
        self.menu = pygame.image.load("assets/hud/menu.png")
        self.option = pygame.image.load("assets/hud/bar-options.png")
        self.lifeBarBack = pygame.image.load("assets/hud/bar-life-back.png")
        self.lifeBarBack2 = pygame.image.load("assets/hud/bar-life-back.png")
        self.cursor = pygame.image.load("assets/others/cursor.png")
                
        self.fundo = pygame.transform.scale(self.fundo, (self.width, 340))
        self.menu = pygame.transform.scale(self.menu, (self.width, 140))
        self.option = pygame.transform.scale(self.option, (self.width // 2, 140))
        self.lifeBarBack = pygame.transform.scale(self.lifeBarBack, (self.width // 2, self.height // 6))
        self.lifeBarBack2 = pygame.transform.scale(self.lifeBarBack2, (self.width // 2, self.height // 6))
        self.cursor = pygame.transform.scale(self.cursor, (self.width // 25, self.height // 20))
        self.pokemon_enemy = pygame.transform.scale(self.enemy_front, (self.width // 5, self.height // 4))
        self.pokemon_player = pygame.transform.scale(self.player_back, (self.width // 5, self.height // 4))

        self.cursor_x, self.cursor_y = 335, 380
        
        pygame.mixer.music.load("musics/Battle!.mp3")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(True)
        
        self.sf_teclas = pygame.mixer.Sound("musics/effects/menu/select.wav")
        self.sf_teclas.set_volume(.7)

        self.enter_pressed = False
        self.key_pressed = False

        self.message = ""
        self.message_time = 0
        self.turn = "player"

    def run(self):
        while True:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.turn == "player":
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
                            damage, message = set_damage(2)
                            self.enemy.takeDamage(damage)
                            self.message = message
                            self.message_time = pygame.time.get_ticks()
                            self.turn = "enemy"
                        elif self.cursor_y == 380 and self.cursor_x == 485:
                            print('mochila')
                        elif self.cursor_y == 425 and self.cursor_x == 335:
                            print('pokemon')
                        elif self.cursor_y == 425 and self.cursor_x == 485:
                            print('fugir')

                if events.type == pygame.KEYUP:
                    self.key_pressed = False

            elif self.turn == "enemy":
                damage, message = set_damage(1)
                self.player.takeDamage(damage)
                self.message = "Enemy's Turn: " + message
                self.message_time = pygame.time.get_ticks()
                self.turn = "player"                

            self.window.blit(self.fundo, (0, 0))
            self.window.blit(self.menu, (0, 340))
            self.window.blit(self.option, (320, 340))
            self.window.blit(self.lifeBarBack, (20, 20))
            self.window.blit(self.lifeBarBack2, (315, 250))

            max_life_width = self.width // 2 - 162
            current_life_width = int((self.player.get_life() / self.player.get_maxLife()) * max_life_width)
            self.lifeBar2 = pygame.transform.scale(pygame.image.load("assets/hud/bar-life.png"), (current_life_width, self.height // 38))
            self.window.blit(self.lifeBar2, (437, 295))

            max_life_width = self.width // 2 - 162
            current_life_width = int((self.enemy.get_life() / self.enemy.get_maxLife()) * max_life_width)
            self.lifeBar = pygame.transform.scale(pygame.image.load("assets/hud/bar-life.png"), (current_life_width, self.height // 38))
            self.window.blit(self.lifeBar, (142, 65))

            fonte = pygame.font.Font('fonts/pokemon_fire_red.ttf', 38)

            enemy_nome_texto = fonte.render(f"{self.enemy_name}", True, (54, 54, 54))
            enemy_nivel_texto = fonte.render(f"{self.enemy_level}", True, (54, 54, 54))
            self.window.blit(enemy_nome_texto, (40, 25))
            self.window.blit(enemy_nivel_texto, (285, 25))
            self.window.blit(self.pokemon_enemy, (400, 80))

            jogador_nome_texto = fonte.render(f"{self.player_name}", True, (54, 54, 54))
            jogador_nivel_texto = fonte.render(f"{self.player_level}", True, (54, 54, 54))
            self.window.blit(jogador_nome_texto, (350, 255))
            self.window.blit(jogador_nivel_texto, (580, 255))
            self.window.blit(self.pokemon_player, (80, 200))

            self.window.blit(self.cursor, (self.cursor_x, self.cursor_y))

            if self.message and pygame.time.get_ticks() - self.message_time < 2000:
                message_text = fonte.render(self.message, True, (255, 255, 255))
                self.window.blit(message_text, (30, 360))
            elif pygame.time.get_ticks() - self.message_time >= 2000:
                self.message = ""

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