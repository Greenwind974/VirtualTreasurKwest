import pygame
import entite
import Joueur

class Projectile(entite.Entite):
    def __init__(self, x, y, width, height, epoque : str, image : pygame.Surface, emmeteur : entite.Entite, vitesse : int, direction : str):
        """
        - pour la direction : Entier entre 0 et 3 : 0 = haut, 1 = droite, 2 = bas, 3 = gauche
        """
        super().__init__(x, y, width, height, epoque, image)
        self.emmeteur = emmeteur
        self.vitesse = vitesse
        self.direction = direction

    def update(self):
        """
        On fait avancer le projectile en fonction de sa direction et de sa vitesse
        """
        if self.direction == "HAUT":
            self.rect.y -= self.vitesse
        elif self.direction == "DROITE":
            self.rect.x += self.vitesse
        elif self.direction == "BAS":
            self.rect.y += self.vitesse
        elif self.direction == "GAUCHE":
            self.rect.x -= self.vitesse

    def onCollide(self, objetCollision):
        """
        Si le projectile est en collision avec un objet bloquant (mur) ou avec lequel il peut interragir (genre le levier pour abaisser le pont levis)
        """
        # On supprime notre objet projectile
        if self in entite.Entite.listProjectile[self.epoque]:
            entite.Entite.listProjectile[self.epoque].remove(self)

    def afficher(self) -> tuple[pygame.Surface, pygame.Rect]:
        return self.image, self.rect
    

if __name__ == "__main__":

    pygame.init()

    screen = pygame.display.set_mode((1300, 800))
    clock = pygame.time.Clock()

    imgJoueur = pygame.image.load("assets/sprite/joueur.png")

    j1 = Joueur.Joueur(0, 0, 0, 0, "PASSE", imgJoueur)
    test1 = Projectile(500, 500, 10, 10, "PASSE", imgJoueur, j1, 5, 0)
    test2 = Projectile(500, 500, 10, 10, "PASSE", imgJoueur, j1, 5, 1)
    test3 = Projectile(500, 500, 10, 10, "PASSE", imgJoueur, j1, 5, 2)
    test4 = Projectile(500, 500, 10, 10, "PASSE", imgJoueur, j1, 5, 3)


    run = True
    while run :
        screen.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        screen.blit(test1.image, test1.rect)
        screen.blit(test2.image, test2.rect)
        screen.blit(test3.image, test3.rect)
        screen.blit(test4.image, test4.rect)
        test1.update()
        test2.update()
        test3.update()
        test4.update()
        
        clock.tick(60)
        pygame.display.flip()

        