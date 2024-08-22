# Disable linting for non-top-level imports
# flake8: noqa: E402
from flask import Flask
from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

import whisper
import pyaudio
import numpy as np
import logging
from googletrans import Translator
from gtts import gTTS
import pygame
import io
import colorlog

# Set up Whisper model
model = whisper.load_model("base")

# Set up PyAudio
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000
BUFFER_SECONDS = 3
ENERGY_THRESHOLD = 0.01

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Set up logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s:%(message)s'))

logger = colorlog.getLogger('whisper_app')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Set up translator
translator = Translator()

# Initialize pygame mixer for audio playback
pygame.mixer.init()

is_listening = False
buffer = []

@socketio.on('connect')
def handle_connect():
  print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
  print('Client disconnected')
  global is_listening
  is_listening = False

@socketio.on('start_listening')
def handle_start_listening():
  global is_listening
  is_listening = True
  socketio.start_background_task(listen_and_transcribe)

@socketio.on('stop_listening')
def handle_stop_listening():
  global is_listening
  is_listening = False

def listen_and_transcribe():
  global is_listening, buffer
  while is_listening:
    try:
      # Capture audio
      audio_chunk = np.frombuffer(
        stream.read(CHUNK, exception_on_overflow=False),
        dtype=np.float32
      )
      buffer.extend(audio_chunk)

      # Process when buffer reaches desired length
      if len(buffer) >= RATE * BUFFER_SECONDS:
        audio_data = np.array(buffer)
        
        if np.abs(audio_data).mean() > ENERGY_THRESHOLD:
          result = model.transcribe(audio_data)

          if result["text"]:
            logger.debug(f"Transcribed audio: {result}")

            # Translate to Korean
            translation = translator.translate(
              result["text"], src="en", dest="ko"
            )
            
            socketio.emit('transcription', {
              'english': result['text'],
              'korean': translation.text
            })

        # Clear buffer
        buffer = []

    except Exception as e:
      print(f"Error in listen_and_transcribe: {e}")


if __name__ == '__main__':
    socketio.run(app, debug=True)
