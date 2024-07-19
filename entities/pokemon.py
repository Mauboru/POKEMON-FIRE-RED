class Pokemon:
    def __init__(self, nome, nivel, life):
        self.__nome = nome
        self.__nivel = nivel
        self.__life = life
        self.__maxLife = life
        
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

    def get_maxLife(self):
        return self.__maxLife
        
    def takeDamage(self, damage):
        self.__life -= damage
        if self.__life < 0:
            self.__life = 0

    def takeHealth(self, life):
        self.__life += life
        if self.__life > self.__maxLife:
            self.__life = self.__maxLife

    def __str__(self):
        return f"Nome: {self.__nome}\nNivel: {self.__nivel}\nVida: {self.__life}\nMaxLife: {self.__maxLife}"