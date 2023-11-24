import openai
import pyaudio
import wave
from pydub import AudioSegment
import os

openAIKey = 'OpenAI Key Here'
elevenLabsKey = 'Eleven Labs Key Here'


class VoiceRecord:
    def __init__(self, openai_key, wav_output_filename="output.wav", mp3_output_filename="output.mp3"):
        self.openai_key = openai_key
        self.wav_output_filename = wav_output_filename
        self.mp3_output_filename = mp3_output_filename

    def record_audio(self, record_seconds=6, format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024):
        audio = pyaudio.PyAudio()

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
        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(self.wav_output_filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

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
    voice_recorder.record_audio()
    transcript = voice_recorder.transcribe_audio()

    print(transcript)
