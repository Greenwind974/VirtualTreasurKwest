import pygame
import entite
import Blaster
import Camera
import moviepy.editor
from SpritesheetManager import spritesheet

class Joueur(entite.Entite):

    def __init__(self, x : int, y : int, width : int, height : int, epoque : str, image : str, controleur : pygame.Surface, vitesse = 8):
        self.controleur = controleur

        if image in spritesheet.ssListe:
            ss = spritesheet.ssListe[image]
        
        else:
            ss = spritesheet(image) # On enleve le .tsx
            spritesheet.ssListe[image] = ss
        
        self.animation = {"DROITE":[],"GAUCHE":[],"HAUT":[],"BAS":[]}
        directions = ["DROITE","GAUCHE","HAUT","BAS"]
        for i in range(4):
            for frame in range(2):
                sprite = ss.image_at((frame*64,i*64,64,64))
                self.animation[directions[i]].append(sprite)

        imgJoueur = pygame.image.load("assets/sprite/joueur.png")
        imgJoueur = self.animation["BAS"][0]

        filename = "assets/sprite/laserBeam.png"
        if filename in spritesheet.ssListe:
            ss = spritesheet.ssListe[filename]
        
        else:
            ss = spritesheet(filename) # On enleve le .tsx
            spritesheet.ssListe[filename] = ss
        

        laserPasse = ss.image_at((0*32, 0, 32, 32))
        laserPresent = ss.image_at((1*32, 0, 32, 32))
        laserFutur = ss.image_at((2*32, 0, 32, 32))
        super().__init__(x, y, width, height, epoque, imgJoueur)
        self.direction = "HAUT" # Entier entre 0 et 3 : 0 = haut, 1 = droite, 2 = bas, 3 = gauche
        lasersPasse = {"HAUT" : pygame.transform.rotate(laserPasse, 90),
                       "BAS" : pygame.transform.rotate(laserPasse, -90),
                       "DROITE" : laserPasse,
                       "GAUCHE" : pygame.transform.flip(laserPasse, True, False)}
        
        lasersPresent = {"HAUT" : pygame.transform.rotate(laserPresent, 90),
                       "BAS" : pygame.transform.rotate(laserPresent, -90),
                       "DROITE" : laserPresent,
                       "GAUCHE" : pygame.transform.flip(laserPresent, True, False)}
        
        lasersFutur = {"HAUT" : pygame.transform.rotate(laserFutur, 90),
                       "BAS" : pygame.transform.rotate(laserFutur, -90),
                       "DROITE" : laserFutur,
                       "GAUCHE" : pygame.transform.flip(laserFutur, True, False)}
        
        self.blasters : dict[str, Blaster.Blaster] = {"PASSE" : Blaster.BlasterPasse(16, lasersPasse, self),
                                                      "PRESENT": Blaster.BlasterPresent(16, lasersPresent, self),
                                                      "FUTUR" : Blaster.BlasterFutur(16, lasersFutur, self)}
        self.blasterChoisi = "FUTUR"
        self.vitesse = vitesse
        # On va stocker les touches de déplacement dans ce dictionnaire des keyPressed
        self.keyPressed = {"HAUT" : False, "DROITE" : False, "BAS" : False, "GAUCHE" : False}
        # Inventaire servant a stocker et a montrer les objets ramassés par le joueur
        self.inventaire = []
        self.changementEpoque = False
        self.orientation = "BAS"
        # Sert à rien mais c'est riogolo
        self.self = self

    def resetKeyPressed(self):
        self.keyPressed = {"HAUT" : False, "DROITE" : False, "BAS" : False, "GAUCHE" : False}

    def onCollide(self, objetCollision : entite.Entite):
        pass

    def checkInterdit(self):
        tileX = self.rect.x//64
        tileY = self.rect.y//64
        
        interdir = False
        if not(0<=tileX<40 and 0<=tileY<80):
            interdir = True

        else:
            """
            print(tileX, tileY)
            print(len(entite.Entite.listMur[self.epoque]))
            print(len(entite.Entite.listMur[self.epoque][tileY]))
            print(entite.Entite.listSol[self.epoque][tileY][tileX].name)"""
            currentTile = entite.Entite.listMur[self.epoque][tileY][tileX]
            if (currentTile and not currentTile.traversable and self.rect.colliderect(currentTile.rect)):
                interdir = True
            currentTile = entite.Entite.listSol[self.epoque][tileY][tileX]
            if (currentTile and not currentTile.traversable and self.rect.colliderect(currentTile.rect)):
                interdir = True
            currentTile = entite.Entite.listDecor[self.epoque][tileY][tileX]
            if (currentTile and not currentTile.traversable and self.rect.colliderect(currentTile.rect)):
                interdir = True

        return interdir

    def update(self, tick):
        """
        """
        self.image = self.animation[self.orientation][(tick%30)//15==0]        
        
        """tileX = self.rect.x//64
        tileY = self.rect.y//64
        currentTile = entite.Entite.listMur[self.epoque][tileY][tileX]
        try:
            print("traversable {} {} {}".format(currentTile.traversable, currentTile.id, currentTile.name))
        except AttributeError:
            print("'NoneType' object has no attribute 'traversable'")
        print(tileX,tileY)"""

        if self.keyPressed["HAUT"]:
            self.rect.y -= self.vitesse
            if self.checkInterdit():
                self.rect.y += self.vitesse
            self.orientation = "HAUT"

        if self.keyPressed["GAUCHE"]:
            self.rect.x -= self.vitesse
            if self.checkInterdit():
                self.rect.x += self.vitesse
            self.orientation = "GAUCHE"

        if self.keyPressed["BAS"]:
            self.rect.y += self.vitesse
            if self.checkInterdit():
                self.rect.y -= self.vitesse
            self.orientation = "BAS"

        if self.keyPressed["DROITE"]:
            self.rect.x += self.vitesse
            if self.checkInterdit():
                self.rect.x -= self.vitesse
            self.orientation = "DROITE"
        

        

        
        


    
    def updateEvent(self, event : pygame.event.Event):
        """
        Va permettre de controler les déplacements du personnage et les tirs de ses blasters
        """
        if event.type == pygame.KEYDOWN:
            # Déplacements
            if event.key == pygame.K_z:
                self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.self.keyPressed["HAUT"] = True
                self.direction = "HAUT"
            elif event.key == pygame.K_q:
                self.keyPressed["GAUCHE"] = True
                self.direction = "GAUCHE"
            elif event.key == pygame.K_s:
                self.keyPressed["BAS"] = True
                self.direction = "BAS"
            elif event.key == pygame.K_d:
                self.keyPressed["DROITE"] = True
                self.direction = "DROITE"
            
            # Tirs avec blasters
            elif event.key == pygame.K_UP:
                self.blasters[self.blasterChoisi].TirerProjectile("HAUT")
            elif event.key == pygame.K_DOWN:
                self.blasters[self.blasterChoisi].TirerProjectile("BAS")
            elif event.key == pygame.K_LEFT:
                self.blasters[self.blasterChoisi].TirerProjectile("GAUCHE")
            elif event.key == pygame.K_RIGHT:
                self.blasters[self.blasterChoisi].TirerProjectile("DROITE")

            # Changement de blaster
            elif event.key == 49: # &
                self.blasterChoisi = "PASSE"
            elif event.key == 50: # é
                self.blasterChoisi = "PRESENT"
            elif event.key == 51: # "
                self.blasterChoisi = "FUTUR"

            # Changment de temporalité
            elif event.key == pygame.K_y: # &
                self.epoque = "PASSE"
                self.changementEpoque = True
            elif event.key == pygame.K_u: # é
                self.epoque = "PRESENT"
                self.changementEpoque = True
            elif event.key == pygame.K_i: # "
                self.epoque = "FUTUR"
                self.changementEpoque = True
            

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                self.keyPressed["HAUT"] = False
            elif event.key == pygame.K_q:
                self.keyPressed["GAUCHE"] = False
            elif event.key ==  pygame.K_s:
                self.keyPressed["BAS"] = False
            elif event.key == pygame.K_d:
                self.keyPressed["DROITE"] = False



if __name__ == "__main__":

    pygame.init()

    screen = pygame.display.set_mode((1300, 800))
    clock = pygame.time.Clock()

    imgJoueur = pygame.image.load("assets/sprite/joueur.png")
    cam = Camera.Camera(0, 0)

    j1 = Joueur(400, 400, 0, 0, "PASSE", imgJoueur, screen, 20)


    run = True
    while run :
        screen.fill("black")

        # Gestion des images
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            j1.updateEvent(event)

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
        
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()