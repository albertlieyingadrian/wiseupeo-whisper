# Wiseupeo Whisper: Real-time Speech Translation (English to Korean, etc)

This project uses OpenAI's Whisper model to transcribe speech in real-time and translate it to another language.

## Features

- Real-time audio capture from microphone
- Speech recognition using Whisper
- Translation between configurable source and target languages
- Text-to-speech output of translated text
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

4. Configure the application:
   Edit `config.json` to set your desired source and target languages, Whisper model, and other parameters.

## Usage

Run the script with:
```
python main.py
```

Speak into your microphone in English. The script will transcribe your speech and translate it to Korean in real-time.

To stop the script, press Ctrl+C.

## Note

This is a basic implementation and may have limitations:
- It processes audio in small chunks, which may affect transcription accuracy.
- Translation is done using an unofficial Google Translate API, which may have usage limits.
- Performance may vary depending on your hardware and internet connection.
