'use client';

import { useState, useEffect } from 'react';
import { Socket, io } from 'socket.io-client';

let socket: typeof Socket | null = null;

interface TranscriptionData {
  english: string;
  korean: string;
}

export default function Home() {
  const [transcription, setTranscription] = useState<string>('');
  const [translation, setTranslation] = useState<string>('');
  const [isListening, setIsListening] = useState<boolean>(false);

  useEffect(() => {
    socket = io('http://localhost:5000');

    socket?.on('connect', () => {
      console.log('Connected to server');
    });

    socket?.on('transcription', (data: TranscriptionData) => {
      setTranscription(data.english);
      setTranslation(data.korean);
    });

    return () => {
      if (socket) {
        socket.off('transcription');
        socket.close();
      }
    };
  }, []);

  const toggleListening = () => {
    if (!socket) return;

    if (isListening) {
      socket.emit('stop_listening');
      setIsListening(false);
    } else {
      socket.emit('start_listening');
      setIsListening(true);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Whisper Playground</h1>
      <button
        onClick={toggleListening}
        className={`px-4 py-2 rounded ${
          isListening ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-500 hover:bg-blue-600'
        } text-white`}
      >
        {isListening ? 'Stop Listening' : 'Start Listening'}
      </button>
      <div className="mt-4">
        <h2 className="text-xl font-semibold">Transcription:</h2>
        <p>{transcription}</p>
      </div>
      <div className="mt-4">
        <h2 className="text-xl font-semibold">Translation:</h2>
        <p>{translation}</p>
      </div>
    </div>
  );
}