import pygame

class Pokemons:

    def __init__(self, id, name, pv, max_pv, type, attack_damage, image_path, sound_path, color, X, Y):
        self.id = id
        self.name = name
        self.pv = pv
        self.max_pv = max_pv
        self.type = type
        self.attack_damage = attack_damage
        self.image_path = image_path
        self.sound_path = sound_path
        self.color = color

        self.image_load = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image_load.get_rect()
        self.rect.x = X
        self.rect.y = Y

    # getters de la class Pokemons

    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getPV(self):
        return self.pv

    def getPvMax(self):
        return self.max_pv

    def getType(self):
        return self.type

    def getAttackDamage(self):
        return self.attack_damage

    def getImagePath(self):
        return self.image_path

    def getImageLoad(self):
        return self.image_load

    def getColor(self):
        return self.color

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y


    # setters de la class Pokemons

    def setID(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setPV(self, pv):
        self.pv = pv

    def setPvMax(self, max_pv):
        self.max_pv = max_pv

    def setType(self, type):
        self.type = type

    def setAttackDamage(self, attack_damage):
        self.attack_damage = attack_damage

    def setImagePath(self, image_path):
        self.image_path = image_path

    def setColor(self, color):
        self.color = color

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y