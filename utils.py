from config import ACCEPTABLE_FILE_TYPES, AUDIO_FILE_PATH
import sounddevice as sd
import soundfile as sf
import os

def is_acceptable_file_type(file):
    for fileType in ACCEPTABLE_FILE_TYPES:
        if file.endswith(fileType):
            return True
    return False


def get_audio_input(duration=8):
    sample_rate = 44100
    print(f"Recording audio for {duration} seconds...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    sf.write(AUDIO_FILE_PATH, audio, sample_rate)
    audio_file = open(AUDIO_FILE_PATH, "rb")
    return audio_file