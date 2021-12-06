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


TextToSpeech("Moohon maaf, sistem tidak terhubung internet",
             'VoiceConnect.mp3')
TextToSpeech("Sistem Monitoring siap digunakan", 'VoiceReady.mp3')
TextToSpeech("Sistem Telah Terhubung Internet Kembali", 'VoiceConnect.mp3')

while True:
    os.system("mpg123 VoiceConnect.mp3")
    time.sleep(3)
