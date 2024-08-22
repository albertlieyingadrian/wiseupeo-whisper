import whisper
import pyaudio
import numpy as np
from googletrans import Translator
import logging
import colorlog
import warnings
from gtts import gTTS
import io
import pygame
import json

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Filter out the specific warning
warnings.filterwarnings("ignore", message="You are using `torch.load` with `weights_only=False`", category=FutureWarning)

# Configure colorlog
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s:%(message)s',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
))

# Set up logging for this script
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Set logging level for all other loggers to INFO
for name in logging.root.manager.loggerDict:
    if name != __name__:
        logging.getLogger(name).setLevel(logging.INFO)

# Load Whisper model
model = whisper.load_model(config['whisper_model'])

logger.debug("Whisper model loaded successfully")

# Initialize PyAudio for microphone input
p = pyaudio.PyAudio()

CHUNK = config['chunk_size']
RATE = config['sample_rate']

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

buffer = []
BUFFER_SECONDS = config['buffer_seconds']

ENERGY_THRESHOLD = config['energy_threshold']

# Initialize translator
translator = Translator()

# Initialize pygame mixer for audio playback
pygame.mixer.init()

print("Listening... (Press Ctrl+C to stop)")
print(f"Source language: {config['source_language']}")
print(f"Target language: {config['target_language']}")

try:
    while True:
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
                
                # Check if the audio energy is above the threshold
                if np.abs(audio_data).mean() > ENERGY_THRESHOLD:
                    result = model.transcribe(audio_data, language=config['source_language'])

                    if result["text"]:
                        logger.debug(f"Transcribed audio: {result}")

                        # Translate to target language
                        translation = translator.translate(
                            result["text"], src=config['source_language'], dest=config['target_language']
                        )
                        
                        print(f"{config['source_language'].upper()}: {result['text']}")
                        print(f"{config['target_language'].upper()}: {translation.text}")
                        print("---")

                        # Convert translated text to speech
                        tts = gTTS(text=translation.text, lang=config['target_language'])
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0) 
                       
                        # Play the generated speech
                        pygame.mixer.music.load(fp)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                else:
                    logger.debug("Silence detected, skipping transcription")

                # Clear buffer
                buffer = []

        except OSError as e:
            logger.warning(f"Audio input error: {e}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            continue

except KeyboardInterrupt:
    print("Stopping...")

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
pygame.mixer.quit()
