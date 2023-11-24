# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:53:58 2023
Modified on 9/15/23 by Luke Renchik
@author: Derek Joslin & Luke Renchik

"""

import openai
import GnomeInterpreter
from voice_to_text import VoiceRecord

openAIKey = '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'
elevenLabsKey = 'f8075f12ddb1ca614af26a0b423269d1'

class Imprint():

    def __init__(self, key, gnomePath):

        # store the api key
        self.response = None
        self.apiKey = key
        openai.api_key = self.apiKey

        # Create the Gnome intrepreter
        self.Gnomes = GnomeInterpreter.GnomeInterpreter()
        self.gnomeList = self.Gnomes.getGnomeKeys()

        # Object Variables
        self.gnome = []
        self.encodedResponse = ""
        self.conversationHistory = []

    def openGnome(self):
        self.gnome = self.Gnomes.getGnome()

    def runGnome(self, prompt):
        self.response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.gnome["intro"]},
                {"role": "user", "content": self.gnome["question"]},
                {"role": "assistant", "content": self.gnome["response"]},
                {"role": "user", "content": prompt},
            ]
        )
        self.encodedResponse = self.response.choices[0].message.content
        return self.encodedResponse

    def createPrompt(self):
        mic = VoiceRecord(openAIKey)
        mic.record_audio()
        userInput = mic.transcribe_audio()
        userInput = userInput["text"]

        prompt = ""

    def startGnome(self, prompt):
        self.conversationHistory = [
            {"role": "system", "content": self.gnome["intro"]},
            {"role": "user", "content": self.gnome["question"]},
            {"role": "assistant", "content": self.gnome["response"]},
        ]
        return self.generateResponse(prompt)

    def generateResponse(self, prompt, memory_data={}):
        # Memory data processing
        memory_intro = ""
        if memory_data:
            name = next(iter(memory_data))
            timestamp = f'{memory_data[name]["timestamp"]}'
            user_input = f'{memory_data[name]["user_input"]}'
            ai_response = f'{memory_data[name]["ai_response"]}'
            memory_intro = (f"Introduction: {self.gnome['intro']}\n\n"
                            f"You have had a previous conversation about this topic with {name}. "
                            f"Please use the following information about the content and time of that conversation "
                            f"to color your current response.\n"
                            f"Timestamp: {timestamp}\n"
                            f"User's Previous Input: {user_input}\n"
                            f"Your Previous Response: {ai_response}")
    
        # Initializing or updating conversation history
        if not hasattr(self, 'conversationHistory'):
            self.conversationHistory = [
                {"role": "system", "content": self.gnome["intro"]},
                {"role": "user", "content": self.gnome["question"]},
                {"role": "assistant", "content": self.gnome["response"]},
            ]
            if memory_intro:
                self.conversationHistory.insert(1, {"role": "system", "content": memory_intro})

        # Appending the user's prompt
        self.conversationHistory.append({"role": "user", "content": prompt})

        # Managing the length of conversationHistory
        if len(self.conversationHistory) > 11:
            self.conversationHistory.pop(1)
            self.conversationHistory.pop(2)

        # Generating the response
        self.response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.conversationHistory
        )
        

        # Assuming the method returns the generated response
        return self.response


