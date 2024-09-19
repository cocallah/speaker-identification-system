# import libraries
import socket
import wave
from pyannote.audio import Pipeline

# receives audio data and save it to a wav file
def receive_and_save_audio(sock, file):
    # specify audio parameters
    audio_format = wave.open(file, 'wb')
    audio_format.setnchannels(1)
    audio_format.setsampwidth(2)
    audio_format.setframerate(44100)
    audio_format.setnframes(0)

    # flag to check if client has terminated
    global flag

    # write audio data to the wav file
    while True:
        data = sock.recv(1024)
        if not data:
            break
        # check if client is done sending audio chunk
        if data.endswith(b'Done'):
            break
        # check if client is terminating the program
        if data.endswith(b'TERMINATE'):
            flag = False
        # write audio data to file
        audio_format.writeframes(data)

    # close the wav file
    audio_format.close()

# initialize speaker identification pipeline
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                    use_auth_token="YOUR_AUTH_TOKEN")

# file names
audio_file = "last_20_seconds.wav"
output_file = "audio_20_seconds.rttm"

# define listening port
PORT = 7007

# create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket
server_socket.bind(('0.0.0.0', PORT))

# listen for incoming connections
server_socket.listen(1)

print("Server is ready")

# accept connection from Raspberry Pi
client_socket, address = server_socket.accept()
print("Connection established with:", address)

# create flag so server knows when to stop
flag = True

# initialize list of speaker counts
speaker_counts = []

while True:

    # Receive and save audio data
    receive_and_save_audio(client_socket, audio_file)

    # break if client has sent message to terminate
    if not flag:
        break

    # apply the pipeline to an audio file
    diarization = pipeline(audio_file)

    # write diarization to output file
    with open(output_file, "w") as rttm:
        diarization.write_rttm(rttm)

    # read the output file to determine the amount of time each speaker spoke
    speakers = {}
    for line in open(output_file):
        line_list = line.split()
        speaker = line_list[7]
        duration = line_list[4]
        speakers[speaker] = speakers.get(speaker, 0) + float(duration)

    # update list of speaker counts for the current audio chunk
    speaker_counts.append(len(speakers))


    # get a list of the durations
    speaker_durations = speakers.values()
    speaker_proportions = [(duration / sum(speaker_durations)) for duration in speaker_durations]

    # scale the speaker data to add up to 8 for the sense hat pixels
    # ensures every speaker that appears is shown with at least 1 pixel
    scaled_numbers = [max(round(proportion * 8), 1) for proportion in speaker_proportions]

    # ensure that the numbers add up to 8
    while sum(scaled_numbers) != 8:
        if sum(scaled_numbers) < 8:
            min_index = scaled_numbers.index(min(scaled_numbers))
            scaled_numbers[min_index] += 1
        else:
            max_index = scaled_numbers.index(max(scaled_numbers))
            scaled_numbers[max_index] -= 1

    # convert numbers to strings
    scaled_strings = [str(num) for num in scaled_numbers]

    # combine into a single string
    number_string = (" ").join(scaled_strings)

    # send information back to client
    client_socket.sendall(number_string.encode("utf-8"))


# close socket
client_socket.close()

# close server
server_socket.close()
