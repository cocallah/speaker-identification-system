## Speaker Identification System
## Rory St. Hilaire (rsthila2@nd.edu) and Conor O'Callahan (cocallah@nd.edu)

# import libraries
import pyaudio
import wave
import time
import numpy as np
from sense_hat import SenseHat

# set audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 700
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "output.wav"

audio = pyaudio.PyAudio()

sense = SenseHat()

# returns true if a loud enough sound is detected
def is_speaking(data):
    numeric_data = np.frombuffer(data, dtype=np.int16)
    avg_amplitude = np.mean(np.abs(numeric_data))
    return avg_amplitude >= THRESHOLD

# makes the sense hat light up green
def show_activity():
    green = [0, 255, 0]
    sense.clear(green)

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer = CHUNK)

print("Listening...")

try:
    # continuously check if speech is detected
    while True:
        data=stream.read(CHUNK)
        if is_speaking(data):
            print("Speaking detected!")
            show_activity()
        else:
            sense.clear()

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
