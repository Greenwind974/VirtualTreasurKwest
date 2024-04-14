import pygame

class Tile():
    pass

class Entite():

    listSol : dict[str, list[list[Tile]]] = {"PASSE" : [], "PRESENT" : [], "FUTUR" : []}
    listMur = {"PASSE" : [], "PRESENT" : [], "FUTUR" : []}
    listDecor = {"PASSE" : [], "PRESENT" : [], "FUTUR" : []}
    listProjectile = {"PASSE" : [], "PRESENT" : [], "FUTUR" : []}
    listAutreEntité = {"PASSE" : [], "PRESENT" : [], "FUTUR" : []}
    joueur = None

    def __init__(self, x, y, width, height, epoque, image : pygame.Surface):
        self.epoque = epoque
        self.image = image
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def updateEvent(self, event : pygame.event.Event):
        """
        """
        #print("Abstract")

    def update(self):
        """
        """
        #print("Abstract")

    def onCollide(self, objetCollision):
        """
        """
        #print("Abstract")

    def afficher(self):
        """
        """
        #print("Abstract")