## Speaker Identification System
## Rory St. Hilaire (rsthila2@nd.edu) and Conor O'Callahan (cocallah@nd.edu)

# import libraries
import speech_recognition as sr
from sense_hat import SenseHat
import wave
import pyaudio

# set audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# create audio object
audio = pyaudio.PyAudio()

# create audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Recording...")

frames = []

# record audio
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording")

stream.stop_stream()
stream.close()
audio.terminate()

# write to wav file
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print("Audio saved")
