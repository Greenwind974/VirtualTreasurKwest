from tile import Tile
import json
from SpritesheetManager import spritesheet
from entite import Entite
from Vue import Vue
import pygame
import Camera 
import Joueur
import ObjetInteractif
import moviepy.editor
from Chat import chat
import time
import cv2

class Controleur():

    def __init__(self):
        self.tick = 0
        self.vue = Vue(self)
        self.camera = Camera.Camera()
        imgJoueur = "assets/sprite/personnage.png"
        
        self.joueurBaseX = 1*64
        self.joueurBaseY = 63*64
        Entite.joueur = Joueur.Joueur(self.joueurBaseX, self.joueurBaseY, 0, 0, "PASSE", imgJoueur, self, 16)
        Entite.joueur.epoque = "FUTUR"
        self.run = True

        self.texteTuto = True
        self.pontBaisse = False
        self.salleOuverte = False
        self.texteIndicePorte = False
        self.fissureCassee = False
        self.texteIndiceFissure = False # permet de savoir s'il faut afficher ou non la textebox pour l'indice de la fissure

        # Création des tiles pour la carte
        self.chargementTuiles()

        image = pygame.image.load("assets/sprite/chat/bebeChat.png")
        Entite.listAutreEntité["PASSE"].append(chat(1328,3072,47,53,"PASSE",image))


        image = pygame.image.load("assets/sprite/chat/chat.png")
        Entite.listAutreEntité["PRESENT"].append(chat(1328,3072,80,80,"PRESENT",image))


        image = pygame.image.load("assets/sprite/chat/chaton1.png")
        Entite.listAutreEntité["FUTUR"].append(chat(1296,3040,46,53,"FUTUR",image))

        image = pygame.image.load("assets/sprite/chat/chaton2.png")
        Entite.listAutreEntité["FUTUR"].append(chat(1440,2880,47,53,"FUTUR",image))

        image = pygame.image.load("assets/sprite/chat/chaton3.png")
        Entite.listAutreEntité["FUTUR"].append(chat(1360,3056,47,53,"FUTUR",image))

        image = pygame.image.load("assets/sprite/chat/chaton4.png")
        Entite.listAutreEntité["FUTUR"].append(chat(1488,3136,47,53,"FUTUR",image))

        image = pygame.image.load("assets/sprite/chat/vieuxChat.png")
        Entite.listAutreEntité["FUTUR"].append(chat(1392,2992,43,50,"FUTUR",image))



    def baisserPont(self):
        self.pontBaisse = True
         
        

        #porte chateau passe
        Entite.listMur["PASSE"][36][19].image = Entite.listMur["PRESENT"][36][19].image
        Entite.listSol["PASSE"][36][19].traversable = True
        Entite.listMur["PASSE"][36][19].traversable = True
        Entite.listMur["PASSE"][36][20].image = Entite.listMur["PRESENT"][36][20].image
        Entite.listSol["PASSE"][36][20].traversable = True
        Entite.listMur["PASSE"][36][20].traversable = True

        Entite.listMur["PASSE"][38][19].image = Entite.listMur["PRESENT"][38][19].image
        Entite.listSol["PASSE"][38][19].traversable = True
        Entite.listMur["PASSE"][38][19].traversable = True
        Entite.listMur["PASSE"][38][20].image = Entite.listMur["PRESENT"][38][20].image
        Entite.listSol["PASSE"][38][20].traversable = True
        Entite.listMur["PASSE"][38][20].traversable = True

        #paillasson chateau passe
        Entite.listSol["PASSE"][39][20].traversable = True
        Entite.listSol["PASSE"][39][19].traversable = True

        pont = Entite.listSol["PRESENT"][40][19].image
        #pont chateau passe
        for i in range(6):
            Entite.listSol["PASSE"][40+i][19].traversable = True  
            Entite.listSol["PASSE"][40+i][19].image = pont  
            Entite.listSol["PASSE"][40+i][20].traversable = True 
            Entite.listSol["PASSE"][40+i][20].image = pont 
        
        Entite.listDecor["PASSE"][42][20].image = pont  
        Entite.listDecor["PASSE"][42][19].image = pont  

    def detruireMurFissure(self):
        self.fissureCassee = True
        
        # On supprime le mur cassable dans dans le passé et dans le présent
        Entite.listMur["PASSE"][15][29] = None
        Entite.listMur["PRESENT"][15][29] = None

        Entite.listMur["PASSE"][15-1][29] = None
        Entite.listMur["PRESENT"][15-1][29] = None

    def afficherIndiceFissure(self):
        self.texteIndiceFissure = True
        print("FAIRE EN SORTE QUE L'INDICE POUR LA FISSURE S'AFFICHE")

    def ouvrirPorteSalle(self):
        self.salleOuverte = True
        print("MODIFIER LA MAP ET LES HITBOX DU PASSE")

    def afficherIndicePorte(self):
        self.texteIndicePorte = True
        print("FAIRE EN SORTE QUE L'INDICE POUR LA PORTE S'AFFICHE")

    def chargementTuiles(self):
        """
            Charge les tuiles suivant le json des tileset
        """

        def ajout(temporalite):
            # Opening JSON file
            f = open('assets/maps/'+temporalite+'.tmj')
            
            # returns JSON object as 
            # a dictionary
            data = json.load(f)
            
            # Iterating through the json
            # list
            dictImg = {0:None} # Format : [id, tile_id] => img (0 => Pas d'image)
            infoTileset = data["tilesets"]
            print(temporalite)
            print(infoTileset)

            for donnee in data["layers"]:
                tile_width = 64
                tile_height = 64
                
                for ligne in range(donnee["height"]):
                    # Ajout de taille dans les tableaux
                    if (donnee["name"]=="sol"):
                        Entite.listSol[temporalite].append([])
                    elif (donnee["name"]=="mur"):
                        Entite.listMur[temporalite].append([])
                    else : 
                        Entite.listDecor[temporalite].append([])


                    for colonne in range(donnee["width"]):
                        

                        id = donnee["data"][ colonne + donnee["width"]*ligne ]
                        donneImg = dictImg.get(id)

                        if (id!=0 and donneImg == None ) : # Pas de tuile et Image à créer 
                            # Retrouver bonne tileset
                            tilesetName = None
                            firstgId = 0
                            i=0
                            while (i<=len(infoTileset)-1 and id>infoTileset[i]["firstgid"]) :
                                firstgId = infoTileset[i]["firstgid"]
                                tilesetName = infoTileset[i]["source"]

                                i += 1
                            
                            filename = "assets/maps/Tileset/"+tilesetName[:-4]+".png"
                            if filename in spritesheet.ssListe:
                                ss = spritesheet.ssListe[filename]
                            
                            else:
                                ss = spritesheet(filename) # On enleve le .tsx
                                spritesheet.ssListe[filename] = ss

                            tile_id = id - firstgId
                            nbColonneSheet = ss.getWidthSheet() / tile_width
                            
                            # Retrouver ligne/colonne de la tuile 
                            ligneTileSheet = tile_id // nbColonneSheet
                            colonneTileSheet = tile_id % nbColonneSheet

                            img = ss.image_at((colonneTileSheet*tile_width, ligneTileSheet*tile_height, tile_width, tile_height))
                            dictImg[id] = [img, tile_id, tilesetName]
                        elif (id!=0):
                            img, tile_id, tilesetName = donneImg

                        # Ajout dans la bonne liste
                        tile = None
                        if (id!=0):
                            tile = Tile(colonne*tile_width, ligne*tile_height, tile_width, tile_height, temporalite, img, tile_id, tilesetName[:-4])
                        else : # Si image vide : tile est None
                            tile = None 
                        if (donnee["name"]=="sol"):
                            Entite.listSol[temporalite][ligne].append(tile)
                        elif (donnee["name"]=="mur"):
                            Entite.listMur[temporalite][ligne].append(tile)
                        else : 
                            Entite.listDecor[temporalite][ligne].append(tile)

            #entree chateau present
            if len(Entite.listSol["PRESENT"]) > 0:

                Entite.listMur["PRESENT"][36][19].traversable = True  
                Entite.listMur["PRESENT"][36][20].traversable = True 
                  
            
            # Closing file
            f.close()

        ajout("PASSE")
        ajout("PRESENT")
        ajout("FUTUR")

        # On ajoute les sprites avec lesquels on peut interagir
        ObjetInteractif.Levier(17*64, 35*64, 10, 10, "PASSE")
        ObjetInteractif.Porte(500, 500, 10, 10, "PASSE")
        ObjetInteractif.Fissure(29*64, 15*64, 10, 10, "PASSE")
        ObjetInteractif.GraineRamassable(300, 400, 10, 10, "PASSE")
        ObjetInteractif.CutterRamassable(300, 400, 10, 10, "FUTUR")


    def changerEpoque(self):
        """
            Changer la view + mettre perso
        """

        #print("FIXER LE BUG VIDEO TRANSITION")
        #video = moviepy.editor.VideoFileClip("assets/SoundTracks/SFX/lalala.mp4")
        #video.preview()
        
        son = pygame.mixer.Sound("assets/SoundTracks/SFX/lalala.mp3")
        son.play()
        duree = son.get_length()
        debut = time.time()

        while (time.time() - debut) < duree:
            video = cv2.VideoCapture('assets/SoundTracks/SFX/lalala.mp4')
            success, video_image = video.read()
            if success :
                video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
                self.vue.screen.blit(video_surf, (self.vue.screenWidth/2 - video_surf.get_width()/2, self.vue.screenHeight/2 - video_surf.get_height()/2))
                pygame.display.flip()
            else :
                pass
        

        Entite.joueur.changementEpoque = False
        Entite.joueur.resetKeyPressed()
        pygame.display.set_mode((self.vue.screenWidth, self.vue.screenHeight))
        Entite.joueur.rect.x , Entite.joueur.rect.y = self.joueurBaseX+64, self.joueurBaseY
        pass
    

    def update(self):
        self.tick += 1
        # Update joueur
        Entite.joueur.update(self.tick)


        # Update collision
        for temporalite in ["PASSE", "PRESENT", "FUTUR"]:
            for p in Entite.listProjectile[temporalite]:
                #detruit si sorti de map

                tileX = p.rect.x//64
                tileY = p.rect.y//64
                
                if not(0<=tileX<40 and 0<=tileY<80):
                    p.onCollide(None)

                else:

                    currentTile = Entite.listMur[temporalite][tileY][tileX]
                    if (currentTile and not currentTile.traversable and p.rect.colliderect(currentTile.rect)):
                        p.onCollide(currentTile)

                    currentTile = Entite.listDecor[temporalite][tileY][tileX]
                    if (currentTile and not currentTile.traversable and p.rect.colliderect(currentTile.rect)):
                        p.onCollide(currentTile)

                
                for autre in Entite.listAutreEntité[temporalite]:
                    if autre.rect.colliderect(p.rect):
                        autre.onCollide(p)
                        p.onCollide(autre)
                

        # Gestion de la caméra
        self.camera.offsetX = Entite.joueur.rect.x + Entite.joueur.rect.width/2 - self.vue.screen.get_width()/2
        self.camera.offsetY = Entite.joueur.rect.y + Entite.joueur.rect.height/2 - self.vue.screen.get_height()/2

        for epoque in Entite.listProjectile.keys():
            for proj in Entite.listProjectile[epoque]:
                proj.update()
        for epoque in Entite.listAutreEntité.keys():
            for ent in Entite.listAutreEntité[epoque]:
                ent.update()

        # Si le joueur a demander à changer de temporalité, on fait l'animation
        if Entite.joueur.changementEpoque :
            self.changerEpoque()

    def updateEvent(self):
        """
            Gestion des events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            Entite.joueur.updateEvent(event)

            for epoque in Entite.listAutreEntité.keys():
                for ent in Entite.listAutreEntité[epoque]:
                    ent.updateEvent(event)

            
            
            Entite.joueur.updateEvent(event)

    def controlerAffichageTextBox(self):
        # Selon la texteBox à afficher on va lancer la bonne fonction d'affichage de textbox
        if self.texteTuto:
            Entite.joueur.resetKeyPressed()
            self.genererTextBoxTuto()
        elif self.texteIndiceFissure:
            Entite.joueur.resetKeyPressed()
            self.genererTextBoxFissure()
        elif self.texteIndicePorte:
            Entite.joueur.resetKeyPressed()
            self.generTextBoxPorte()
    
    def genererTextBoxTuto(self):
        # Paramètre qui permet de changer la largeur des textBox créées par cette fonction
        textBoxwidth = 900
        textFontSize = 18

        # On affiche le bandeau en haut du textBox (ouais c'est pas très beau mais bon voilà)
        self.vue.afficherTextBox("Bonjour et bienvenue dans VTK : Virtual Treasure Kwest",
                                 (self.vue.screen.get_width()/2 - textBoxwidth/2, 80), textBoxwidth, 22, True)
        self.vue.afficherTextBox(" ",
                                 (self.vue.screen.get_width()/2 - textBoxwidth/2, 110), textBoxwidth, textFontSize, True)
        
        listeMessages = ["Ce jeu est un jeu d'engimes sur le thème du voyage dans le temps.",
                         "Votre quete est de trouver un trésor caché dans un complexe construit ",
                         " au dessus des ruines d'un chateau fort.",
                         "Dans ce jeu vous allez être amenés à voyager plusieurs fois entre différentes",
                         "temporalités : passé, présent et futur, sur la même zone.",
                         "Vous disposez aussi de 3 blasters : un tirant uniquement dans le passé, un autre",
                         "dans le présent et le dernier dans le futur.",
                         "A noter que par exemple, vous pouvez tirer avec le blaster du passé en étant",
                         "dans le présent et le tir partira dans le passé.",
                         "Instant tuto :",
                         "- vous pouvez vous déplacer avec les touche Z,Q,S,D de votre clavier",
                         "- vous pouvez interagir avec le monde, avec la touche E",
                         "- vous pouvez utiliser les touches &, é et \" pour changer de blaster de",
                         "dimension respective passé, présent, futur",
                         "- vous pouvez changer de temporalité en utilisant les touches Y, U et I",
                         "pour aller dans le passé, le présent, le futur",
                         "Appuyez sur E pour fermer les fenêtres de dialogue."]
        
        # On affiche toutes les lignes de texte
        for i in range(len(listeMessages)):
            self.vue.afficherTextBox(listeMessages[i],
                                 (self.vue.screen.get_width()/2 - textBoxwidth/2, 130 + i*2*textFontSize), textBoxwidth, textFontSize)




    def genererTextBoxFissure(self):
        self.vue.afficherTextBox("Ce mur semble avoir été fragile fut un temps, mais est désormais réparé", 
                                 (self.vue.screen.get_width()/2 - 500, self.vue.screen.get_height()/2 - 10),
                                 1000, 20, True)

    def generTextBoxPorte(self):
        self.vue.afficherTextBox("Cette porte est fermée et trop solide pour mon blaster", 
                                 (self.vue.screen.get_width()/2 - 450, self.vue.screen.get_height()/2 - 10 - 20),
                                 900, 20, False)
        self.vue.afficherTextBox("Je devrais trouver la clé ! Ou bien de quoi la découper...", 
                                 (self.vue.screen.get_width()/2 - 450, self.vue.screen.get_height()/2 - 10 + 20),
                                 900, 20, False)
        
    def updateTextBox(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.texteIndiceFissure = False
                    self.texteIndicePorte = False
                    self.texteTuto = False
    
    def afficher(self) :
        """
            Affichage
        """
        # Affichage des l'entité
        self.vue.afficherListeTuiles(Entite.listSol[Entite.joueur.epoque], self.camera)
        self.vue.afficherListeTuiles(Entite.listMur[Entite.joueur.epoque], self.camera)
        self.vue.afficherListeTuiles(Entite.listDecor[Entite.joueur.epoque], self.camera)

        self.vue.afficherListeImages(Entite.listAutreEntité[Entite.joueur.epoque], self.camera)
        self.vue.afficherListeImages(Entite.listProjectile[Entite.joueur.epoque], self.camera)
        
        self.vue.afficherImage(Entite.joueur.image, Entite.joueur.rect, self.camera)

        # Affichage ui
        self.vue.afficherUI(Entite.joueur.blasterChoisi, Entite.joueur.inventaire)

        self.controlerAffichageTextBox()

        self.vue.updateScreen()



if __name__ == "__main__" :
    c = Controleur()


    cam = Camera.Camera()

    # Test des objets interactifs
    ObjetInteractif.GraineRamassable(600, 100, 10, 10, "FUTUR")
    ObjetInteractif.CutterRamassable(100, 150, 10, 10, "PRESENT")
    ObjetInteractif.CutterRamassable(100, 600, 10, 10, "PASSE")
    

    c.run = True

    # A laisser, permet de bien initialiser la map et tout, puis de mettre la popup de tuto
    c.updateEvent()
    c.update()

    c.afficher()

    while c.run:
        c.vue.screen.fill("black")

        if c.texteIndiceFissure or c.texteIndicePorte or c.texteTuto :
            c.updateTextBox()
        else:
            c.updateEvent()
            c.update()

        c.afficher()