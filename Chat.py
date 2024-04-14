from entite import Entite
from time import time
import os
from pygame import mixer
from random import choice

class chat(Entite):
    cooldown = time()
    miaulement = []

    def __init__(self,x,y,width,height,epoque,image):
        super().__init__(x, y, width, height, epoque, image)
        chat.cooldown = time()

        if len(chat.miaulement) == 0:
            for i in os.listdir("assets/SoundTracks/SFX/miaou"):
                if i.split(".")[1] == "mp3":
                    chat.miaulement.append(i)

    
    def update(self):
        if self.rect.colliderect(Entite.joueur.rect) and time()>chat.cooldown and self.epoque == Entite.joueur.epoque:
            chat.cooldown = time() + 2
            choix = choice(chat.miaulement)
            chemin = "assets/SoundTracks/SFX/miaou/" + choix
            mixer.Sound(chemin).play()
            print("Remerciement a {} pour son enregistrement".format(choix.split(".")[0]))