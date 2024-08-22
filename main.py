import whisper
import pyaudio
import numpy as np
from googletrans import Translator
import logging
import colorlog
import warnings

# Filter out the specific warning
warnings.filterwarnings("ignore", message="You are using `torch.load` with `weights_only=False`", category=FutureWarning)

# Load Whisper model
model = whisper.load_model("base")

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

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[handler]
)

# Set logging level for all other loggers to INFO
for name in logging.root.manager.loggerDict:
    if name != __name__:
        logging.getLogger(name).setLevel(logging.INFO)

logger.debug("Whisper model loaded successfully")

# Initialize PyAudio for microphone input
p = pyaudio.PyAudio()

CHUNK = 4096  # Start with a smaller chunk size
RATE = 16000  # Keep the sample rate at 16kHz for Whisper

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

buffer = []
BUFFER_SECONDS = 1  # Collect 1 second of audio before processing

# Add this constant near the top of the file, after other constants
ENERGY_THRESHOLD = 0.01  # Adjust this value based on your microphone and environment

# Initialize translator
translator = Translator()

print("Listening... (Press Ctrl+C to stop)")

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
                    result = model.transcribe(audio_data)

                    if result["text"]:
                        logger.debug(f"Transcribed audio: {result}")

                        # Translate to Korean
                        translation = translator.translate(
                            result["text"], src="en", dest="ko"
                        )
                        
                        print(f"English: {result['text']}")
                        print(f"Korean: {translation.text}")
                        print("---")
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
