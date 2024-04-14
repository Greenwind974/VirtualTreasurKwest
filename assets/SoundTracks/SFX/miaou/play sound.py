import pygame
import os
from random import choice
import time

pygame.init()

nom = []
for i in os.listdir():
    if i.split(".")[1] == "mp3":
        nom.append(i)

while True:
    choix = choice(nom)
    sound = pygame.mixer.Sound(choix)
    sound.play()

    temps = sound.get_length()
    print("{} joué en {}s".format(choix,temps))
    time.sleep(temps)

