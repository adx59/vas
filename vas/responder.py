#!/usr/bin/env python
from threading import Thread
from queue import Queue 
from io import BytesIO

from gtts import gTTS
import pydub
from pydub.playback import play

class Responder: 
    def __init__(self, parent):
        self.parent = parent

    def say(self, speech: str):
        audio_bytes = BytesIO()

        audio = gTTS(speech)
        audio.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        aud_play = pydub.AudioSegment.from_file(audio_bytes, format="mp3")
        play(aud_play)

    def launch(self):
        print('[LOAD] Responder module has been loaded and activated!')
    