import sounddevice as sd
import soundfile as sf

import os
import openai
from langchain.llms import OpenAI
from config import SHADOW_AGENT_TEMP, SHADOW_AGENT_LLM






def record_audio(duration, sample_rate):
    print(f"Recording audio for {duration} seconds...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    return audio

def save_audio(audio, file_path, sample_rate):
    print(f"Saving audio to {file_path}...")
    sf.write(file_path, audio, sample_rate)





duration = float(input("Enter recording duration in seconds: "))
sample_rate = 44100  # Default sample rate (CD quality)

audio = record_audio(duration, sample_rate)


file_path = input("Enter the file path to save the audio (including .wav extension): ")
save_audio(audio, file_path, sample_rate)

print("Audio recording saved successfully.")

# openai.api_key = "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"

from dotenv import load_dotenv
load_dotenv(".env")

# print(os.getenv("OPENAI_API_KEY"))

openai.api_key = os.getenv("OPENAI_API_KEY")


# _llm = OpenAI(temperature=SHADOW_AGENT_TEMP, model=SHADOW_AGENT_LLM)
# res =  _llm("capital of france is?")
# print(res)


audio_file = open("sampleaudio.wav", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript.text)

# main()
