import os
import time
from gtts import gTTS


def TextToSpeech(phrase, format):
    try:
        language = 'id'
        output = gTTS(text=phrase, lang=language, slow=False)
        output.save(format)
        return True
    except Exception as error:
        print("SoundOutput Error")


TextToSpeech("Sistem menutup atap Otomatis", "VoiceTutupAtap.mp3")
TextToSpeech("Sistem membuka atap Otomatis", "VoiceBukaAtap.mp3")

while True:
    os.system("mpg123 VoiceTutupAtap.mp3")
    time.sleep(3)
    os.system("mpg123 VoiceBukaAtap.mp3")
    time.sleep(2)
