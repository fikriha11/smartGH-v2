from typing import Text
from gtts import gTTS
from playsound import playsound

def output (phrase):
    my_text = phrase    
    language = 'id'
    output = gTTS(text=my_text, lang=language, slow=False)   
    output.save('temp.mp3')
    playsound("temp.mp3")
    return True



