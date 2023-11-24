import openai
import pyaudio
import wave
from pydub import AudioSegment
import os
import time

openAIKey = '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'
elevenLabsKey = 'f8075f12ddb1ca614af26a0b423269d1'


class VoiceRecord:
    def __init__(self, openai_key, wav_output_filename="output.wav", mp3_output_filename="output.mp3"):
        self.openai_key = openai_key
        self.wav_output_filename = wav_output_filename
        self.mp3_output_filename = mp3_output_filename
        
        
        # audio variables
        self.recordSeconds = 6
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        
        

    # Start audio recording
    def startAudioRecord(self):
        self.audio = pyaudio.PyAudio()

        # start recording audio
        self.stream = self.audio.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk)

        print("Recording...")
        
        # start a timer
        self.recordSeconds = time.perf_counter()
    
    # End audio recording
    def endAudioRecord(self):
        self.recordSeconds = time.perf_counter() - self.recordSeconds
        
        # pack audio data
        self.frames = []
        for _ in range(0, int(self.rate / self.chunk * self.recordSeconds)):
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        
        
        # stop recording audio
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        
        print("Finished recording.")
    
    # Process audio
    def processAudio(self):
        # create audio wav file
        with wave.open(self.wav_output_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        # convert to mp3
        audio_segment = AudioSegment.from_wav(self.wav_output_filename)
        audio_segment.export(self.mp3_output_filename, format="mp3")
        

    def record_audio(self, record_seconds=6, format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024):
        audio = pyaudio.PyAudio()

        # start recording audio
        stream = audio.open(format=format,
                            channels=channels,
                            rate=rate,
                            input=True,
                            frames_per_buffer=chunk)

        print("Recording...")
 
        
        frames = []
        
        
        
        for _ in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)

        

        print("Finished recording.")
        # stop recording audio
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # 
        with wave.open(self.wav_output_filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        # 
        audio_segment = AudioSegment.from_wav(self.wav_output_filename)
        audio_segment.export(self.mp3_output_filename, format="mp3")

    def transcribe_audio(self):
        if not os.path.exists(self.mp3_output_filename):
            raise FileNotFoundError(f"The file '{self.mp3_output_filename}' does not exist.")

        with open(self.mp3_output_filename, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file, api_key=self.openai_key)

        return transcript


if __name__ == "__main__":
    openAIKey = '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'

    voice_recorder = VoiceRecord(openAIKey)
    # voice_recorder.record_audio()
    voice_recorder.startAudioRecord()
    
    time.sleep(3)
    
    voice_recorder.endAudioRecord()
    voice_recorder.processAudio()
    
    transcript = voice_recorder.transcribe_audio()

    print(transcript)
