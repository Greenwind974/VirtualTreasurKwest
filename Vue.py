import pygame
from SpritesheetManager import spritesheet

class Vue():

    def __init__(self, controleur) -> None:
        self.controleur = controleur
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock() # faire .tick(60) pour avoir 60fps
        pygame.display.set_caption("VTK : Virtual Treasure Kwest")
        self.screenWidth = 1300
        self.screenHeight = 800
        self.screen = pygame.display.set_mode( (self.screenWidth, self.screenHeight) )
        self.baseFontSize = 18
        self.fontSize = self.baseFontSize
        self.fontFilePath = "assets/font/ZenDots-Regular.ttf"
        self.font = pygame.font.Font(self.fontFilePath, self.fontSize)

    def afficherImage(self, image : pygame.Surface, rect : pygame.Rect, cam):
        """
        permet d'afficher une image/surface pygame sur la fenêtre principale
        """
        rectCopy = rect.copy()
        rectCopy.x -= cam.offsetX
        rectCopy.y -= cam.offsetY
        self.screen.blit(image, rectCopy)

    def afficherListeImages(self, lstEntites, camera):
        """
            Affiche les entités (sauf les tuiles)
        """
        for i in range(len(lstEntites)):
            self.afficherImage(lstEntites[i].image, lstEntites[i].rect, camera)

    def afficherListeTuiles(self, lstTiles, camera):
        """
            Affiche les tuiles
        """
        for l in range(len(lstTiles)):
            for c in range(len(lstTiles[l])):
                if lstTiles[l][c] :
                    self.afficherImage( lstTiles[l][c].image, lstTiles[l][c].rect, camera)
        
    def afficherTextBox(self, texte : str, position : tuple[int, int], largeur : int, fontSize = 0, centered = False):
        """
        Permet d'afficher un un zone de texte, dans une zone de la largeur indiquée, avec retour à la ligne automatique
        ( la largeur pas encore implémenté )
        """
        # On redéfini la font, selon la taille choisie par l'utilisateur
        if fontSize:
            self.fontSize = fontSize
        else:
            self.fontSize = self.baseFontSize
        self.font = pygame.font.Font(self.fontFilePath, self.fontSize)

        # Texte
        texteSurface : pygame.Surface = self.font.render(texte, True, "white")
        rect = texteSurface.get_rect()
        #rect.width = largeur

        # Fond du texte
        rectBg = rect.copy()
        rectBg.x = position[0]
        rectBg.y = position[1]
        rectBg.width = largeur
        rectBg.height += 20
        pygame.draw.rect(self.screen, "blue", rectBg)

        if centered:
            rect.x = rectBg.x + rectBg.width/2 - rect.width/2
            rect.y = rectBg.y + rectBg.height/2 - rect.height/2
        else :
            rect.x += rectBg.x + 10
            rect.y += rectBg.y + 10

        self.screen.blit(texteSurface, rect)

    @staticmethod
    def create_rect(width, height, border, color, border_color):
        surf = pygame.Surface((width+border*2, height+border*2), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (border, border, width, height), 0)
        for i in range(1, border):
            pygame.draw.rect(surf, border_color, (border-i, border-i, width+5, height+5), 1)
        return surf

    def afficherUI(self, blasterChoisi, inventaire):
        """
            Affichage de l'interface
        """
        ### Inventaire des Blasters
        # Surface de l'inventaire

        invBlasters = pygame.Surface((300, 100))
        wInv = invBlasters.get_width()
        hInv = invBlasters.get_height()
        color = (255,255,255)
        invBlasters.fill(color)


        for i in range(3):
            colorFond = (100,100,100)
            if ( (blasterChoisi=="PASSE" and i==0) or
                 (blasterChoisi=="PRESENT" and i==1) or 
                 (blasterChoisi=="FUTUR" and i==2) ):
                border_color = (0,0,0)
            else:
                border_color = (100, 100, 100)
            blasterIconsBorder = Vue.create_rect(80, 80, 5, colorFond, border_color)
            wIcon = blasterIconsBorder.get_width()
            hIcon = blasterIconsBorder.get_height()
            ecart = (wInv-wIcon*3)/4

            filename = "assets/sprite/laserBeam.png"
            
            if filename in spritesheet.ssListe:
                ss = spritesheet.ssListe[filename]
            
            else:
                ss = spritesheet(filename) # On enleve le .tsx
                spritesheet.ssListe[filename] = ss

            img = ss.image_at((i*32, 0, 32, 32))
            img = pygame.transform.scale(img, (64, 64))
            blasterIconsBorder.blit(img, ((wIcon-64)/2,(wIcon-64)/2 ) )

            invBlasters.blit(blasterIconsBorder, ((wIcon+ecart)*i + ecart, (hInv-hIcon)/2) )

        self.screen.blit(invBlasters, ( (self.screenWidth-wInv )/2, self.screenHeight-hInv - 20))

        ### Inventaire des items
        # Surface de l'inventaire
        invItems = pygame.Surface((100, 200))
        wInv = invItems.get_width()
        hInv = invItems.get_height()
        color = (255,255,255)
        invItems.fill(color)

        nbObjetMax = 2
        for i in range(nbObjetMax):
            colorFond = (100,100,100)
            border_color = (100, 100, 100)
            itemsIconsBorder = Vue.create_rect(80, 80, 5, colorFond, border_color)
            wIcon = itemsIconsBorder.get_width()
            hIcon = itemsIconsBorder.get_height()
            ecart = (hInv-hIcon*nbObjetMax)/(nbObjetMax+1)

            if i<len(inventaire): # Affichage de l'objet
                img = inventaire[i].image
                img = pygame.transform.scale(img, (64, 64))
                itemsIconsBorder.blit(img, ((wIcon-64)/2,(wIcon-64)/2 ) )

            invItems.blit(itemsIconsBorder, (ecart, (hIcon+ecart)*i + ecart ) )

            self.screen.blit(invItems, ( 20, (self.screenHeight-hInv)/2))



    def updateScreen(self):
        """
        a appeler en fin de mainloop
        """

        self.clock.tick(60)
        pygame.display.flip()


        





if __name__ == "__main__":

    vueJeu = Vue("michel")

    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        vueJeu.afficherTextBox("Coucou les gensaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", (200, 200), 500)

        pygame.draw.circle(vueJeu.screen, "red", (50, 50), 40, 4)

        vueJeu.updateScreen()
        
