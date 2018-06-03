import pygame

def playBeep(soundclip='audio/beep.mp3'):
    pygame.mixer.init()
    pygame.mixer.music.load(soundclip)
    pygame.mixer.music.play()
    
    return
