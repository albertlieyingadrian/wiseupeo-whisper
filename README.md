# Whisper Playground: Real-time English to Korean Translation

This project uses OpenAI's Whisper model to transcribe English speech in real-time and translate it to Korean.

## Features

- Real-time audio capture from microphone
- Speech recognition using Whisper
- Translation from English to Korean
- Continuous operation with easy termination

## Requirements

- Python 3.7+
- See `requirements.txt` for Python package dependencies
- PortAudio (for PyAudio)

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/whisper-playground.git
   cd whisper-playground
   ```

2. Install PortAudio (required for PyAudio):
   - On macOS (using Homebrew):
     ```
     brew install portaudio
     ```
   - On Ubuntu/Debian:
     ```
     sudo apt-get install portaudio19-dev
     ```
   - On Windows: No additional step required, but you might need to install Visual C++ Build Tools if you encounter issues.

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script with:

```
python whisper_playground.py
```

Speak into your microphone in English. The script will transcribe your speech and translate it to Korean in real-time.

To stop the script, press Ctrl+C.

## Note

This is a basic implementation and may have limitations:
- It processes audio in small chunks, which may affect transcription accuracy.
- Translation is done using an unofficial Google Translate API, which may have usage limits.
- Performance may vary depending on your hardware and internet connection.