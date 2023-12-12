class Pokemon:
    def __init__(self, nome, sprite, nivel):
        self.__nome = nome
        self.__sprite = sprite
        self.__nivel = nivel
        
    def get_nome(self):
        return self.__nome
    
    def set_nome(self, nome):
        self.__nome = nome
    
    def get_sprite(self):
        return self.__sprite
    
    def set_sprite(self, sprite):
        self.__sprite = sprite
    
    def get_nivel(self):
        return self.__nivel
    
    def set_nivel(self, nivel):
        self.__nivel = nivel