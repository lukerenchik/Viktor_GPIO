import tkinter as tk
from GPIODetector import HardwareInterface
from VoiceRecord import VoiceRecord
from VoiceSynthesizer import VoiceSynthesizer
import Viktor as vik

import time
openAIKey = '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'
elevenLabsKey = 'f8075f12ddb1ca614af26a0b423269d1'
myAI = vik.Viktor(openAIKey, elevenLabsKey)
# from PIL import Image, ImageTk
# from Viktor import Viktor


# myAI = Viktor(openAIKey, elevenLabsKey)

# container for ai responses
class AIResponseWindow():
    
    def __init__(self):
        # create the tkinter window
        self.win = tk.Tk()
        self.win.title("Viktor.AI")
        self.win.geometry("1200x900")
        
        # tkinter string for user query
        self.userQuery = tk.StringVar()
        
        # tkinter string for ai state 
        self.aiState = tk.StringVar()
        
        # tkinter string for ai response 
        self.aiResponse = tk.StringVar()
        self.aiResponse.set("nice to meet you!")

        # user box title
        userQueryTitleLabel = tk.Label(self.win, text="User Query", font=('DSEG', 16, "bold"))
        userQueryTitleLabel.pack()
        
        # create a label for the user query
        userQueryLabel = tk.Label(self.win, textvariable=self.userQuery, font=('Helvetica', 16, "bold"), wraplength=1050)
        userQueryLabel.pack(pady=30)
        
        # create a label to display ai state
        aiStateLabel = tk.Label(self.win, textvariable=self.aiState, font=('Helvetica', 16, "bold"), wraplength=1050)
        aiStateLabel.pack(pady=30)
        
        # ai state title
        aiStateTitleLabel = tk.Label(self.win, text="Viktor's Response", font=('DSEG', 16, "bold"))
        aiStateTitleLabel.pack()
        
        # create a label to display the ai response
        aiResponseLabel = tk.Label(self.win, textvariable=self.aiResponse, font=('Orbitron', 16, "bold"), wraplength=1050)
        aiResponseLabel.pack(pady=30)
        
        # add the update button
        updateButton = tk.Button(self.win, text="Talk to Viktor", command=self.guiPress)
        updateButton.pack(pady=5)
    
    def guiPress(self):
        self.aiResponse.set("gui Press")

# Open the image and resize it to 700x500 pixels
# image = Image.open("victor.gif")
# image = image.resize((1200, 600))
# tk_image = ImageTk.PhotoImage(image)

# Create a Label for displaying the image
# image_label = tk.Label(win, image=tk_image)
# image_label.pack()

# create a global ai response window
mainWindow = AIResponseWindow()
# AiVoice = VoiceSynthesizer(elevenLabsKey)

class VictorButton(HardwareInterface):
    
    def __init__(self, _pinNumber, _VoiceRecorder):
        # do super class initializer
        super().__init__(_pinNumber)
        
        # add the voice recorder as an property
        self.VoiceRecorder = _VoiceRecorder

    def buttonPressed(self, nButtonPresses):
		# add stuff here
        pressString = f"this is luke's button function pressed {nButtonPresses} times"
        print(pressString)

        # update the state string
        mainWindow.aiState.set("Viktor is listening")
        
        # begin recording the audio
        self.VoiceRecorder.startAudioRecord()
        
    def buttonReleased(self, nButtonReleases):
		# add stuff here
        releaseString = f"this is luke's button function released {nButtonReleases} times"
        print(releaseString)
        
        # end the audio recording
        startTime = time.perf_counter()
        
        self.VoiceRecorder.endAudioRecord()
        self.VoiceRecorder.processAudio()
        
        # print the time it took to process the audio
        print("audio process time")
        print(time.perf_counter() - startTime)
        startTime = time.perf_counter()
        
        # call the whisper api call
        transcript = self.VoiceRecorder.transcribe_audio()
        
        print("openai whisper time")
        print(time.perf_counter() - startTime)
        
        # update the ai response label
        mainWindow.userQuery.set(transcript["text"])
        
        # update the state string
        mainWindow.aiState.set("Viktor is thinking...")
        
        # query for names and keywords in user string
        keywords, names= myAI.identify_names_keywords(transcript)

        #check if previous conversations about the topic has occured
        memory_data = myAI.memoryKeywordCheck(names, keywords)

        # send the query to viktor
        aiReply = myAI.getResponse(transcript, memory_data)

        mainWindow.aiResponse = aiReply

        

        # grab viktor's response and get the audio
        mainWindow.aiState.set("Viktor is speaking!")
        myAI.voiceStream(aiReply)
        print(time.perf_counter() - startTime)
        startTime = time.perf_counter()
        
        
        
        # play audio
        # play the audio response
        

if __name__ == "__main__":

    PIN_NUMBER = 5
    
    voiceRecorder = VoiceRecord(openAIKey)
    
    VicButton = VictorButton(PIN_NUMBER, voiceRecorder)
    VicButton.createButtonThread()
    

    mainWindow.win.mainloop()
