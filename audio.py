from gtts import gTTS
import pygame
import os

def audio_path(word: str) -> str:
    return "audio/" + word.replace(" ", "_") + ".mp3"

def download_audio(word: str) -> None:
    path = audio_path(word)
    if not os.path.isfile(path):
        myobj = gTTS(text=word, lang='en', slow=False)
        myobj.save(path)

def delete_audio(word: str) -> None:
    path = audio_path(word)
    if os.path.isfile(path):
        os.remove(path)

def play_audio(word: str) -> None:
    path = audio_path(word)
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()