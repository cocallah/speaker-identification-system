## Speaker Identification System
## Rory St. Hilaire and Conor O'Callahan

import pyaudio
import numpy as np
from scipy.signal import hamming
from sense_hat import SenseHat

# set audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
THRESHOLD = 600
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "output.wav"

audio = pyaudio.PyAudio()

sense = SenseHat()

# set window
window = hamming(CHUNK)

# check if sound is detected
def is_speaking(data):
    numeric_data = np.frombuffer(data, dtype=np.int16)
    avg_amplitude = np.mean(np.abs(numeric_data))
    return avg_amplitude >= THRESHOLD

# calculate the most dominant frequency in the audio data
def calculate_pitch(data):
    windowed_data = data * window

    spectrum = np.fft.fft(windowed_data, n=CHUNK)

    freqs = np.fft.fftfreq(len(spectrum), 1/RATE)
    positive_freqs = freqs[:len(spectrum)//2]

    magnitude_spectrum = np.abs(spectrum[:len(spectrum)//2])

    freq_indices = np.where((positive_freqs >= 85) & (positive_freqs <= 255))[0]
    if len(freq_indices) > 0:

        magnitudes_within_range = magnitude_spectrum[freq_indices]
        frequencies_within_range = positive_freqs[freq_indices]

        max_magnitude_index = np.argmax(magnitudes_within_range)
        pitch_hz = frequencies_within_range[max_magnitude_index]
    else:
        pitch_hz = 0
    return pitch_hz

# calculate sense hat display based on pitch (red for low pitch, blue for high pitch)
def map_pitch_to_color(pitch_hz):
    min_pitch = 85
    max_pitch = 255
    min_color = [255, 0, 0]
    max_color = [0, 0, 255]

    normalized_pitch = (pitch_hz - min_pitch) / (max_pitch - min_pitch)
    color = [
        int(min_color[i] + normalized_pitch * (max_color[i] - min_color[i]))
        for i in range(3)
    ]
    return color

def show_activity(color):
    sense.clear(color)

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Listening...")

try:
    # continously check for sound
    while True:
        data = stream.read(CHUNK)
        if is_speaking(data):
            print("Speaking detected!")
            pitch_hz = calculate_pitch(np.frombuffer(data, dtype=np.int16))
            print(pitch_hz)
            color = map_pitch_to_color(pitch_hz)
            print(color)
            show_activity(color)
        else:
            sense.clear()

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
