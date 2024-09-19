## client application for final project
## Rory St. Hilaire & Conor O'Callahan

# import libraries

from sense_hat import SenseHat
import wave
import pyaudio
import socket

# setup pyaudio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

# sensehat setup
speakers = [[255, 0, 0],
            [0, 255, 0],
            [0, 0, 255],
            [255, 255, 0],
            [255, 0, 255],
            [0, 255, 255],
            [255, 255, 255],
            [255, 165, 0]]

sense = SenseHat()
sense.clear()

# control the lighting on the SenseHat FIXME
def lightup(sense, speaker_data):
    # make the message from the server into a list for pixel setting
    speaker_data = speaker_data.split()
    for i in range(len(speaker_data)):
        speaker_data[i] = int(speaker_data[i])
    speaker_data = sorted(speaker_data)

    # build the column from the message data
    new_column = []
    speaker = 0
    for elem in speaker_data:
        for i in range(elem):
            new_column.append(speakers[speaker])
        speaker += 1

    # light up the new column and shift the old columns to the left
    for x in range(8):
        for y in range(8):
            if x == 7:
                sense.set_pixel(x, y, new_column[y][0], 
                                new_column[y][1], new_column[y][2])
            else:
                pixel_color = sense.get_pixel(x+1, y)
                sense.set_pixel(x, y, pixel_color[0], pixel_color[1],
                                pixel_color[2])


# function that will terminate the program after the current while loop iteration
flag = True
def terminate(event):
    global flag
    if event.action == 'pressed':
        flag = False
        
sense.stick.direction_any = terminate

# server information
server_ip = "192.168.0.18"
server_port = 7007

# set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))
client_socket.settimeout(20000)

while flag:
    # create audio stream
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording...")

    # make wave file
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        client_socket.sendall(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    client_socket.sendall(b'Done')

    response = client_socket.recv(1024).decode("utf-8")
    lightup(sense, str(response))

message = b'TERMINATE'
client_socket.sendall(message)



