import os
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


def soundOutput():
    try:
        phrase = f"Selamat datang, Kondisi Suhu ruangan sekarang adalah {200} derajat Celcius, dan Kelembapan udara mencapai {100} Persen."
        phrase1 = f"Untuk Keterangan Cahaya Sebesar {100} Lumen, Terima Kasih"
        language = 'id'
        output = gTTS(text=phrase + phrase1, lang=language, slow=False)
        output.save('temp.mp3')
        # song = AudioSegment.from_mp3('temp.mp3')
        # play(song)
        os.system("mpg123 temp.mp3")
        return True
    except Exception as error:
        print("SoundOutput Error")


while True:
    soundOutput()
