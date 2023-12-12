class Pokemon:
    def __init__(self, nome, nivel, life):
        self.__nome = nome
        self.__nivel = nivel
        self.__life = life * nivel
        
    def get_nome(self):
        return self.__nome
    
    def set_nome(self, nome):
        self.__nome = nome
    
    def get_nivel(self):
        return self.__nivel
    
    def set_nivel(self, nivel):
        self.__nivel = nivel
        
    def get_life(self):
        return self.__life
    
    def set_life(self, life):
        self.__life = life
        
    def __str__(self):
        return f"{self.__nome}\n{self.__nivel}\n{self.__life}"