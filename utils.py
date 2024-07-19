import pygame, random, requests, io

pygame.init()

sf_attack1 = pygame.mixer.Sound("assets/musics/effects/battle/firered_000C.wav")
sf_attack2 = pygame.mixer.Sound("assets/musics/effects/battle/firered_000D.wav")
sf_life = pygame.mixer.Sound("assets/musics/effects/health.wav")

def get_pokemon(largura, altura):
    try:
        numero = random.randint(1, 898)
        api = f"https://pokeapi.co/api/v2/pokemon/{numero}/"
        response = requests.get(api)
        dados = response.json()

        # Info do pokemon
        front = dados['sprites']['versions']['generation-v']['black-white']['animated']['front_default']
        back = dados['sprites']['versions']['generation-v']['black-white']['animated']['back_default']
        nome = dados['name']
        nivel = random.randint(1, 10)
        life = random.randint(12, 36)

        response_imagem = requests.get(front)
        imagem_bytes = io.BytesIO(response_imagem.content)

        sprite_front = pygame.image.load(imagem_bytes)
        sprite_front = pygame.transform.scale(sprite_front, (largura // 4, altura // 4))

        response_imagem = requests.get(back)
        imagem_bytes = io.BytesIO(response_imagem.content)

        sprite_back = pygame.image.load(imagem_bytes)
        sprite_back = pygame.transform.scale(sprite_back, (largura // 4, altura // 4))
        return sprite_front, sprite_back, nome, nivel, life
    except Exception as e:
        print(f"Erro ao carregar o sprite: {e}")
        return get_pokemon(largura, altura)

def key_down(evento, key):
    if evento.type == pygame.KEYDOWN:
        if evento.key == key:
            return True
    return False

def set_volume_for_sounds(sounds, volume):
    for sound in sounds:
        sound.set_volume(volume)

def get_initials_pokemons(largura, altura):
    pokemons = []
    for _ in range(3):
        pokemons.append(get_pokemon(largura, altura))
    return pokemons

def set_damage(damage):
    d20 = random.randint(1, 20)
    if d20 > 1 and d20 < 20:
        message = "SUCCESSFUL"
        sf_attack2.play()
        return damage, message
    elif d20 == 1:
        message = "MISS"
        return 0, message
    else:
        message = "CRITICAL ATTACK"
        sf_attack1.play()
        return damage * 2, message
    
def set_life(life, level):
    d4 = random.randint(1, 4)
    message = f"{d4 * level} WAS INCREASED IN YOUR LIFE!"
    sf_life.play()
    return life * level, message

# -->=