import pygame
import Joueur
import entite
import Projectile

class Blaster(entite.Entite):
    def __init__(self, epoque, vitesse, imagesProjectiles : dict[str, Projectile.Projectile], joueur):
        """
        """
        super().__init__(joueur.rect.x, joueur.rect.y, joueur.rect.width, joueur.rect.height, epoque, pygame.image.load("assets/sprite/joueur.png"))
        self.joueur : Joueur.Joueur = joueur
        self.vitesseProj = vitesse
        self.imagesProjectiles : dict[str, Projectile.Projectile] = imagesProjectiles
    
    def TirerProjectile(self, direction : str):
        """
        méthode virtuelle
        """

class BlasterPasse(Blaster):
    def __init__(self, vitesse, imagesProjectiles : dict[str, Projectile.Projectile], joueur):
        super().__init__("PASSE", vitesse, imagesProjectiles, joueur)

    def TirerProjectile(self, direction : str):
        """
        ajouter un projectile dans la liste des projectiles du passé
        """
        entite.Entite.listProjectile[self.epoque].append(Projectile.Projectile(self.joueur.rect.x, self.joueur.rect.y,
                                                                           10, 10,
                                                                           self.epoque, # Le blaster tire bien dans SON époque
                                                                           self.imagesProjectiles[direction],
                                                                           self.joueur, self.vitesseProj, direction))

class BlasterPresent(Blaster):
    def __init__(self, vitesse, imagesProjectiles : dict[str, Projectile.Projectile], joueur):
        super().__init__("PRESENT", vitesse, imagesProjectiles, joueur)

    def TirerProjectile(self, direction : str):
        """
        ajouter un projectile dans la liste des projectiles du passé
        """
        entite.Entite.listProjectile[self.epoque].append(Projectile.Projectile(self.joueur.rect.x, self.joueur.rect.y,
                                                                           10, 10,
                                                                           self.epoque, # Le blaster tire bien dans SON époque
                                                                           self.imagesProjectiles[direction],
                                                                           self.joueur, self.vitesseProj, direction))

class BlasterFutur(Blaster):
    def __init__(self, vitesse, imagesProjectiles : dict[str, Projectile.Projectile], joueur):
        super().__init__("FUTUR", vitesse, imagesProjectiles, joueur)

    def TirerProjectile(self, direction : str):
        """
        ajouter un projectile dans la liste des projectiles du passé
        """
        entite.Entite.listProjectile[self.epoque].append(Projectile.Projectile(self.joueur.rect.x, self.joueur.rect.y,
                                                                           10, 10,
                                                                           self.epoque, # Le blaster tire bien dans SON époque
                                                                           self.imagesProjectiles[direction],
                                                                           self.joueur, self.vitesseProj, direction))


if __name__ == "__main__":

    pygame.init()

    screen = pygame.display.set_mode((1300, 800))
    clock = pygame.time.Clock()

    imgJoueur = pygame.image.load("assets/sprite/joueur.png")

    j1 = Joueur.Joueur(400, 400, 0, 0, "PASSE", imgJoueur)
    j2 = Joueur.Joueur(400, 400, 0, 0, "PASSE", imgJoueur)
    j2.direction = 1
    j3 = Joueur.Joueur(400, 400, 0, 0, "PASSE", imgJoueur)
    j3.direction = 2
    j4 = Joueur.Joueur(400, 400, 0, 0, "PASSE", imgJoueur)
    j4.direction = 3
    
    b1 = BlasterPasse(12, imgJoueur, j1)
    b2 = BlasterPresent(12, imgJoueur, j2)
    b3 = BlasterFutur(12, imgJoueur, j3)
    b4 = BlasterPasse(12, imgJoueur, j4)


    run = True
    while run :
        screen.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                b1.TirerProjectile()
                b2.TirerProjectile()
                b3.TirerProjectile()
                b4.TirerProjectile()
        
        for epoque in ["PASSE", "PRESENT", "FUTUR"]:
            for tir in entite.Entite.listProjectile[epoque]:
                tir.update()
                screen.blit(tir.image, tir.rect)
        
        clock.tick(60)
        pygame.display.flip()