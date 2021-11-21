from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


def output(phrase):
    try:
        language = 'id'
        output = gTTS(text=phrase, lang=language, slow=False)
        output.save('temp.wav')

        song = AudioSegment.from_mp3('temp.wav')
        play(song)
        return True
    except Exception as error:
        print(error)
