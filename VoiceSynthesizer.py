# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 20:26:44 2023

@author: Derek Joslin

"""

import requests
import pygame
import io

class VoiceSynthesizer():

    def __init__(self, apiKey):
        # initialize the api key
        self.headers = {
            "accept": "audio/mpeg",
            "xi-api-key": apiKey,
            "Content-Type": "application/json",
        }

        self.url = 'https://api.elevenlabs.io/v1/text-to-speech/T4hWaNL0H6B2PLnt9ST0'

        pygame.mixer.init()

    def synthVoice(self, voiceString):
        data = {
          "text": voiceString,
          "voice_id": "T4hWaNL0H6B2PLnt9ST0",
          "voice_settings": {
            "stability": 0.25,
            "similarity_boost": 0.95
          }
        }

        
        response = requests.post(self.url, headers=self.headers, json=data)
        print(response.content)
        self.audioBytes = response.content

    def playSound(self):
        audioBuffer = io.BytesIO(self.audioBytes)
        pygame.mixer.music.load(audioBuffer)
        # pygame.mixer.music.load(audioBuffer)
        pygame.mixer.music.play()
# =============================================================================
#     def playSound(self):
#         audio = AudioSegment.from_file(io.BytesIO(self.audioBytes), format="mp3")
#         play(audio)
#         while pygame.mixer.music.get_busy():
#@                pygame.time.Clock().tick(10)
# =============================================================================
# =============================================================================
#     def playSound(self):
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
#             f.write(self.audioBytes)
#             f.flush()
#             playsound(f.name)
# 
# =============================================================================

