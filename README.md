Conor O'Callahan,
Rory St. Hilaire

# Summary
Our project implements a speaker identification system to identify the number
of speakers participating in a conversation. Additionally, our system can provide
live feedback that shows what proportion of the conversation each speaker contributed.
With these analytics, users will be able to identify patterns in conversations and
their interactions with others. To implement this functionality, we made a client
program that runs on a Raspberry Pi that sends audio data to a server program for
processing and reporting back to the client program so that it can display the live
feedback.

# server.py
This contains the server that runs on the laptop. Uses the PyAnnote library to
download a pretrained speaker diarization model. Receives audio from the client
and uses wave library to save it to a .wav file. The diarization model processes
the .wav file, and then the server sends the information back to the client

# finalClient.py
This contains the client code that runs on the Raspberry Pi. Reads in audio data
from microphone using PyAudio library and sends audio data to the server. It then
waits for a response from the server and uses that response to determine the
appropriate Sense HAT lighting

# listen.py, pitch.py, project.py
These files contain our initial attempts to record audio and implement Sense HAT
compatibility.
