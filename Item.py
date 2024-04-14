import pygame

class Item:
    
    def __init__(self, nom : str, image : pygame.Surface) -> None:
        self.nom = nom
        self.image = image