import pygame, random, requests, io

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
        return sprite_front, nome, nivel, life
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