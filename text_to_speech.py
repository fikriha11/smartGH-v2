from gtts import gTTS
from playsound import playsound

def output (phrase):   
    language = 'id'
    output = gTTS(text=phrase, lang=language, slow=False)   
    output.save('temp.mp3')
    playsound('temp.mp3')
    return True



