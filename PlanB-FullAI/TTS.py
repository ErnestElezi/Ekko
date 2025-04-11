from gtts import gTTS
from playsound import playsound


def speak(words: str):
    tts = gTTS(words)
    tts.save('hello.mp3')
    playsound("C:/Users/user/Game Folders/Coding/Ekko/hello.mp3")
