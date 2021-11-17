from typing import Text
from gtts import gTTS
from playsound import playsound


my_text = 'Selamat datang di Greenhouse, Suhu Sekarang adalah 23 Derajat Celcius'
language = 'id'
output = gTTS(text=my_text, lang=language, slow=False)
output.save('temp.mp3')
playsound('temp.mp3')
