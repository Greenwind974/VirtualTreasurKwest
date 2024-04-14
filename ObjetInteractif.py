import pygame
import entite
import Item
from SpritesheetManager import spritesheet
import Projectile

class ObjetInteractif(entite.Entite):
    def __init__(self, x, y, width, height, epoque, imageItem: pygame.Surface):
        super().__init__(x, y, width, height, epoque, imageItem)
        self.listeEpoques = [epoque] #est utilse pour les objets devant être affichés dans plusieurs époques différentes
        entite.Entite.listAutreEntité[epoque].append(self)

    def updateEvent(self, event):
        """
        Si la touche "E" est appuyée (touche d'interaction) ou bien si le joueur se dirige vers l'objet, déclenche l'interaction si le joueur est assez proche
        """
        # On vérifie d'abord que le joueur est bien dans la même époque que l'objet
        if entite.Entite.joueur.epoque not in self.listeEpoques:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.actionEvent()
                
    def update(self):
        if True in entite.Entite.joueur.keyPressed.values():
            self.actionEvent()

    def actionEvent(self):
        rectInteractionJoueur : pygame.Rect = entite.Entite.joueur.rect.copy()
        rectInteractionJoueur.width = 50
        rectInteractionJoueur.height = 50
        if entite.Entite.joueur.direction == "HAUT":
            rectInteractionJoueur.midbottom = entite.Entite.joueur.rect.center
        elif entite.Entite.joueur.direction == "DROITE":
            rectInteractionJoueur.midleft = entite.Entite.joueur.rect.center
        elif entite.Entite.joueur.direction == "BAS":
            rectInteractionJoueur.midtop = entite.Entite.joueur.rect.center
        elif entite.Entite.joueur.direction == "GAUCHE":
            rectInteractionJoueur.midright = entite.Entite.joueur.rect.center

        if rectInteractionJoueur.colliderect(self.rect):
            self.interaction()
        
    def interaction(self):
        """
        Abstrait
        """

class Levier(ObjetInteractif):
    def __init__(self, x, y, width, height, epoque):
        self.ss = spritesheet("assets/sprite/levier.png") # Spritesheet
        super().__init__(x, y, width, height, epoque, self.ss.image_at((0, 0*32, 64, 64)))
        self.listeEpoques.append("PRESENT")
        entite.Entite.listAutreEntité["PRESENT"].append(self) # il est utilisable uniquement dans le passé mais visible dans le présent

    def interaction(self):
        # On change le levier, si l'interaction se fait dans la meme temporalité que notre
        self.image = self.ss.image_at((0, 64, 64, 32))

        entite.Entite.joueur.controleur.baisserPont()

    def actionEvent(self):
        if entite.Entite.joueur.epoque == self.epoque:
            rectInteractionJoueur : pygame.Rect = entite.Entite.joueur.rect.copy()
            rectInteractionJoueur.width = 50
            rectInteractionJoueur.height = 50
            if entite.Entite.joueur.direction == "HAUT":
                rectInteractionJoueur.midbottom = entite.Entite.joueur.rect.center
            elif entite.Entite.joueur.direction == "DROITE":
                rectInteractionJoueur.midleft = entite.Entite.joueur.rect.center
            elif entite.Entite.joueur.direction == "BAS":
                rectInteractionJoueur.midtop = entite.Entite.joueur.rect.center
            elif entite.Entite.joueur.direction == "GAUCHE":
                rectInteractionJoueur.midright = entite.Entite.joueur.rect.center

            if rectInteractionJoueur.colliderect(self.rect):
                self.interaction()
    
    def onCollide(self, objetCollision):
        # En cas de collision avec un tir de blaster de la même époque que notre levier, il change d'état
        if type(objetCollision) == Projectile.Projectile and objetCollision.epoque == self.epoque:
            self.interaction()


class Porte(ObjetInteractif):
    def __init__(self, x, y, width, height, epoque):
        # Le joueur va pouvoir interragir avec la porte, mais du coup le sprite utilisé sera un sprite invisible, car c'est la map qui sera changée
        super().__init__(x, y, width, height, epoque, pygame.image.load("assets/sprite/dalek.png"))

    def interaction(self):
        # La porte va pouvoir soit afficher le message à l'utilisateur que la porte est fermée et qu'il faut touver un mouen de l'ouvrir,
        #soit elle va s'ouvrir s'il a le cutter laser
        
        for item in entite.Entite.joueur.inventaire:
            if item.nom == "Cutter Laser":
                entite.Entite.joueur.controleur.ouvrirPorteSalle()
                return
        
        entite.Entite.joueur.controleur.afficherIndicePorte()


class Fissure(ObjetInteractif):
    def __init__(self, x, y, width, height, epoque):
        # Le joueur va pouvoir interragir avec la porte, mais du coup le sprite utilisé sera un sprite invisible, car c'est la map qui sera changée
        super().__init__(x, y, width, height, epoque, pygame.image.load("assets/sprite/vide.png"))
        self.listeEpoques.append("PRESENT")
        entite.Entite.listAutreEntité["PRESENT"].append(self) # il est destructible uniquement dans le passé mais il est référencé dans le présent pour interragir avec.

    def interaction(self):
        # Si le joueur interragi avec la fissure dans le présent il va avoir un indice
        if entite.Entite.joueur.epoque == "PRESENT":
            entite.Entite.joueur.controleur.afficherIndiceFissure()

    def onCollide(self, objetCollision):
        # En cas de collision avec un tir de blaster de la même époque que notre fissure, le mur au meme endroit est censé être détruit
        if type(objetCollision) == Projectile.Projectile and objetCollision.epoque == self.epoque:
            entite.Entite.joueur.controleur.detruireMurFissure()



class ObjetRammassable(ObjetInteractif):

    def __init__(self, x, y, width, height, epoque, imageItem: pygame.Surface):
        super().__init__(x, y, width, height, epoque, imageItem)
        self.item = None

    def interaction(self):
        """
        l'objet va dans l'inventaire du joueur
        """
        print("rammassé")
        entite.Entite.joueur.inventaire.append(self.item)
        entite.Entite.listAutreEntité[self.epoque].remove(self)

class GraineRamassable(ObjetRammassable):

    def __init__(self, x, y, width, height, epoque):
        super().__init__(x, y, width, height, epoque, pygame.image.load("assets/sprite/dalek.png"))
        self.item = Item.Item("Graine", self.image)

class CutterRamassable(ObjetRammassable):

    def __init__(self, x, y, width, height, epoque):
        super().__init__(x, y, width, height, epoque,
                         pygame.transform.smoothscale(pygame.image.load("assets/sprite/laser.png"), (40, 40)))
        self.item = Item.Item("Cutter Laser", self.image)


if __name__ == "__main__":
    import Joueur
    import Camera

    pygame.init()

    screen = pygame.display.set_mode((1300, 800))
    clock = pygame.time.Clock()

    imgJoueur = pygame.image.load("assets/sprite/joueur.png")
    cam = Camera.Camera()

    j1 = Joueur.Joueur(400, 400, 0, 0, "FUTUR", imgJoueur, 20)
    entite.Entite.joueur = j1


    # Test des objets interactifs
    GraineRamassable(600, 100, 10, 10, "FUTUR")
    CutterRamassable(100, 150, 10, 10, "PRESENT")
    CutterRamassable(100, 600, 10, 10, "PASSE")


    run = True
    while run :
        screen.fill("black")

        # Gestion des images
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            j1.updateEvent(event)

            for epoque in entite.Entite.listAutreEntité.keys():
                for ent in entite.Entite.listAutreEntité[epoque]:
                    ent.updateEvent(event)

        j1.update()

        # Affichage
        # On modifie le rect récupéré pour l'offset avec la camera
        cam.offsetX = j1.rect.x + j1.rect.width/2 - screen.get_width()/2
        cam.offsetY = j1.rect.y + j1.rect.height/2 - screen.get_height()/2

        rectJ = j1.rect.copy()
        rectJ.x, rectJ.y = screen.get_width()/2 - j1.rect.width/2, screen.get_height()/2 - j1.rect.height/2
        screen.blit(j1.image, rectJ)
        
        for epoque in entite.Entite.listProjectile.keys():
            for proj in entite.Entite.listProjectile[epoque]:
                proj.update()
                # On modifie le rect récupéré pour l'offset avec la camera
                rect = proj.rect.copy()
                rect.x -= cam.offsetX
                rect.y -= cam.offsetY
                # On affiche
                screen.blit(proj.image, rect)

        for epoque in entite.Entite.listAutreEntité.keys():
            for ent in entite.Entite.listAutreEntité[epoque]:
                ent.update()
                # On modifie le rect récupéré pour l'offset avec la camera
                rect = ent.rect.copy()
                rect.x -= cam.offsetX
                rect.y -= cam.offsetY
                # On affiche
                screen.blit(ent.image, rect)
        
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()