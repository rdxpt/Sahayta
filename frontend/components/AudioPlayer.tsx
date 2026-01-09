import React, { useEffect, useRef } from 'react';

interface AudioPlayerProps {
  audioChunks: string[]; // Base64 encoded audio chunks
  isPlaying: boolean;
}

export const AudioPlayer: React.FC<AudioPlayerProps> = ({ audioChunks, isPlaying }) => {
  const audioContextRef = useRef<AudioContext | null>(null);
  const sourceRef = useRef<AudioBufferSourceNode | null>(null);

  useEffect(() => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
    }

    if (audioChunks.length === 0) return;

    const playAudioChunk = async (base64: string) => {
      try {
        const binaryString = atob(base64);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }

        const audioBuffer = await audioContextRef.current!.decodeAudioData(bytes.buffer);
        const source = audioContextRef.current!.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioContextRef.current!.destination);
        source.start(0);
        sourceRef.current = source;
      } catch (error) {
        console.error('Error playing audio chunk:', error);
      }
    };

    if (isPlaying && audioChunks.length > 0) {
      playAudioChunk(audioChunks[audioChunks.length - 1]);
    }
  }, [audioChunks, isPlaying]);

  return null; // Audio is handled via Web Audio API
};
