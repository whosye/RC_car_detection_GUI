import pygame 
import os 

path_sound = os.path.join(os.path.abspath('Sound'),'win.mp3')
pygame.mixer.init()
pygame.mixer.music.load(path_sound)
pygame.mixer.music.play()

