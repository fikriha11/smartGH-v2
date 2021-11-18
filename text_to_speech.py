from gtts import gTTS
from pygame import mixer

def output (phrase):
    language = 'id'
    output = gTTS(text=phrase, lang=language, slow=False)   
    output.save('temp.mp3')
    mixer.init()    
    mixer.music.load("temp.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    while mixer.music.get_busy() == True:
        continue
    mixer.music.stop()
    return True



