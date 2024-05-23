import pygame, random, requests, io

def get_pokemon(largura, altura):
    try:
        numero = random.randint(1, 898)
        api = f"https://pokeapi.co/api/v2/pokemon/{numero}/"
        response = requests.get(api)
        dados = response.json()

        # Info do pokemon
        sprite_url = dados['sprites']['versions']['generation-v']['black-white']['animated']['front_default']
        nome = dados['name']
        nivel = random.randint(1, 10)

        response_imagem = requests.get(sprite_url)
        imagem_bytes = io.BytesIO(response_imagem.content)
        sprite = pygame.image.load(imagem_bytes)
        sprite = pygame.transform.scale(sprite, (largura // 4, altura // 4))
        return sprite, nome, nivel
    except Exception as e:
        print(f"Erro ao carregar o sprite: {e}")
        return get_pokemon(largura, altura)

def key_down(evento, key):
    if evento.type == pygame.KEYDOWN:
        if evento.key == key:
            return True
    return False