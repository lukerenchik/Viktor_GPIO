import openai
import GPT_API_Interactions as im
from termcolor import colored
from voice_to_text import VoiceRecord
import time
from datetime import datetime
import pytz
import spacy
import json
from elevenlabs import generate, stream, set_api_key

est = pytz.timezone('US/Eastern')
macGnome = "/Users/user/Documents/AIDev_Luke_WD/gnomes/ViktorTest.gnome"
piGnome = "/home/lukerenchik/Documents/AIDev_Luke/gnomes/ViktorTest.gnome"
macSummarized = '/Users/user/Documents/AIDev_Luke_WD/gnomes/SummarizedConversations.gnome'
nlp = spacy.load("en_core_web_lg")
voiceID = "a0jAm3ze3RlUbJTTOd5C"
openAIKey = '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'
elevenLabsKey = 'f8075f12ddb1ca614af26a0b423269d1'

set_api_key(elevenLabsKey)

def print_large_unicode(text, color='red', attrs=['bold']):
    print(colored(text, color, attrs=attrs))


class Viktor(im.Imprint):

    def __init__(self, openAIKey, elevenLabsKey):
        # create the imprint of Viktor
        super().__init__(openAIKey, macGnome)
        self.openGnome()

    def getUserInput(self):
        mic = VoiceRecord(openAIKey)
        mic.record_audio()
        userInput = mic.transcribe_audio()
        userInput = userInput["text"]
        return userInput

    def saveConversation(self, userInput, aiResponse, names, keywords):
        viktors_memories = macSummarized

        #Timestamp for Gnome Dictionary
        current_time_est = datetime.now(est)
        formatted_time = current_time_est.strftime('%Y-%m-%d %H:%M:%S')

        try:
            with open(viktors_memories, "r") as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {}  
                
        for name in names:
            if name not in data:
                data[name] = {}
            data[name]["timestamp"] = formatted_time
            data[name]["user_input"] = userInput
            data[name]["ai_response"] = aiResponse
            data[name]["keywords"] = keywords
            #print(data)
        with open(viktors_memories, 'w') as file:
            json.dump(data, file, indent=4)  
        
    def identify_names_keywords(self, text):
        doc = nlp(text)
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        if names:
            print("Recognized names:", ', '.join(names))
        else:
            print("No names recognized in the provided text.")

        keywords = [token.text for token in doc if token.pos_ in ["NOUN", "VERB"]]
        return keywords, names

    def memoryKeywordCheck(self, name_list, keyword_list):
            # Load the data from SummarizedConversations.gnome file
        with open('/Users/user/Documents/AIDev_Luke_WD/gnomes/SummarizedConversations.gnome', 'r') as file:
            data = json.load(file)
    
        # Dictionary to hold the matches
        matches = {}

        # Iterate through the names in the name_list
        for name in name_list:
            # Check if the name exists in the data
            if name in data:
                # Get the keywords associated with the name from the data
                data_keywords = set(data[name]["keywords"])
                # Convert the keyword_list to a set for comparison
                input_keywords = set(keyword_list)
                # Find the common keywords
                common_keywords = data_keywords.intersection(input_keywords)
                # Check if 50% or more of the input keywords are in the data keywords
                if len(common_keywords) >= len(input_keywords) * 0.5:
                    # If so, add the entry to the matches dictionary
                    matches[name] = {
                        "timestamp": data[name]["timestamp"],
                        "user_input": data[name]["user_input"],
                        "ai_response": data[name]["ai_response"]
                    }
        return matches

    def startConversation(self):
        self.openGnome()
        mic = VoiceRecord(openAIKey)
        mic.record_audio()
        userInput = mic.transcribe_audio()
        userInput = userInput["text"]
        print(userInput)

        #Testing Zone
        keywords, names = self.identify_names_keywords(userInput)
        #print(names)
        #print(keywords)
        memory_data = self.memoryKeywordCheck(names, keywords)
      



        print("Viktor is thinking...")
        genericResponse = self.startGnome(userInput)
        genericResponse = self.response["choices"][0]["message"]["content"]
        print(genericResponse)
        self.voiceStream(genericResponse)
        print("\n")
        keywords, names =self.identify_names_keywords(genericResponse)
        self.saveConversation(userInput, genericResponse, names, keywords)
        return genericResponse

    def talkToAI(self):
        self.openGnome()
        mic = VoiceRecord(openAIKey)
        mic.record_audio()
        userInput = mic.transcribe_audio()
        userInput = userInput["text"]
        print(userInput)
        print("Viktor is thinking...")
        genericResponse = self.generateResponse(userInput)
        genericResponse = self.response["choices"][0]["message"]["content"]
        print(genericResponse)
        self.voiceStream(genericResponse) 
        self.saveConversation(userInput, genericResponse, names, keywords)
        return genericResponse

    def voiceStream(self, genericResponse):
        audio_stream = generate(text = genericResponse, stream = True, voice=voiceID, model="eleven_multilingual_v2", latency=4)
        stream(audio_stream= audio_stream)

    def getResponse(self, userInput, memory_data):
        self.openGnome()
        genericResponse = self.generateResponse(userInput, memory_data)
        genericResponse = self.response["choices"][0]["message"]["content"]
        return genericResponse

if __name__ == "__main__":

    myAI = Viktor(openAIKey, elevenLabsKey)
    response = myAI.startConversation()
    keywords, names = myAI.identify_names_keywords(response)

    #print(keywords)
    #print(names)
    time.sleep(10)

    while 1:
        response = myAI.talkToAI()
        myAI.identify_names_keywords(response)
        time.sleep(10)
