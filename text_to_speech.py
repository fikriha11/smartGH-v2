import pygame
from typing import Text
from gtts import gTTS

def output (phrase):
    my_text = phrase    
    language = 'id'
    output = gTTS(text=my_text, lang=language, slow=False)   
    output.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    return True



