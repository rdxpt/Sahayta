import React, { useState, useEffect, useRef, useCallback } from 'react';
import Head from 'next/head';
import { GlassmorphismDialpad } from '../components/GlassmorphismDialpad';
import { IntelligenceFeed } from '../components/IntelligenceFeed';
import { SovereigntyMeter } from '../components/SovereigntyMeter';
import { AudioPlayer } from '../components/AudioPlayer';
import { LiveGrievanceReport } from '../components/LiveGrievanceReport';

interface SummaryItem {
  type: 'intent' | 'entity' | 'action';
  label: string;
  value: string;
  timestamp: number;
}

export default function Home() {
  const [isCallActive, setIsCallActive] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [summaryItems, setSummaryItems] = useState<SummaryItem[]>([]);
  const [websocketMessages, setWebsocketMessages] = useState<any[]>([]);
  const [audioChunks, setAudioChunks] = useState<string[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isWipingMemory, setIsWipingMemory] = useState(false);
  const [dataPointsStored, setDataPointsStored] = useState(0);
  const socketRef = useRef<WebSocket | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);

  // Initialize WebSocket
  useEffect(() => {
    if (isCallActive) {
      connectWebSocket();
    } else {
      disconnectWebSocket();
    }

    return () => {
      disconnectWebSocket();
    };
  }, [isCallActive]);

  const connectWebSocket = useCallback(() => {
    setIsLoading(true);
    
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//localhost:8000/ws/call`;

    try {
      socketRef.current = new WebSocket(wsUrl);

      socketRef.current.onopen = () => {
        console.log('WebSocket connected');
        setIsLoading(false);
        setIsProcessing(true);
        startAudioStream();
      };

      socketRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);

        // Store all messages for LiveGrievanceReport
        setWebsocketMessages((prev) => [...prev, data]);

        if (data.type === 'text_chunk') {
          setSummaryItems((prev) => [
            ...prev,
            {
              type: data.category || 'intent',
              label: data.label || 'Response',
              value: data.text,
              timestamp: Date.now(),
            },
          ]);
        } else if (data.type === 'audio_chunk') {
          setAudioChunks((prev) => [...prev, data.audio]);
        } else if (data.type === 'data_count') {
          setDataPointsStored(data.count);
        } else if (data.type === 'memory_wipe_start') {
          setIsWipingMemory(true);
        } else if (data.type === 'memory_wipe_complete') {
          setIsWipingMemory(false);
          setDataPointsStored(0);
        } else if (data.type === 'call_complete') {
          setIsProcessing(false);
        }
      };

      socketRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsLoading(false);
        handleCallEnd();
      };

      socketRef.current.onclose = () => {
        console.log('WebSocket disconnected');
      };
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
      setIsLoading(false);
    }
  }, []);

  const disconnectWebSocket = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      mediaStreamRef.current = null;
    }
  }, []);

  const startAudioStream = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStreamRef.current = stream;

      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const source = audioContext.createMediaStreamSource(stream);
      const processor = audioContext.createScriptProcessor(4096, 1, 1);

      source.connect(processor);
      processor.connect(audioContext.destination);

      processor.onaudioprocess = (event) => {
        const audioData = event.inputBuffer.getChannelData(0);
        const base64Audio = btoa(String.fromCharCode(...new Uint8Array(audioData.buffer)));

        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
          socketRef.current.send(
            JSON.stringify({
              type: 'audio_chunk',
              audio: base64Audio,
            })
          );
        }
      };
    } catch (error) {
      console.error('Failed to access microphone:', error);
      handleCallEnd();
    }
  };

  const handleCallStart = () => {
    setIsCallActive(true);
    setSummaryItems([]);
    setWebsocketMessages([]);
    setAudioChunks([]);
    setDataPointsStored(0);
  };

  const handleCallEnd = () => {
    setIsCallActive(false);
    setIsProcessing(false);
    setIsWipingMemory(false);
    disconnectWebSocket();
  };

  return (
    <>
      <Head>
        <title>MCD 311 - Sovereign Voice AI</title>
        <meta name="description" content="Data-Sovereign Grievance Redressal System" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="flex h-screen bg-gradient-to-br from-sovereign-dark to-sovereign-light">
        {/* Left Panel - Live Grievance Report */}
        <div className="w-96 border-r border-gray-700/50 p-6 flex flex-col overflow-hidden">
          <LiveGrievanceReport 
            websocketData={websocketMessages} 
            isCallActive={isCallActive}
          />
        </div>

        {/* Center Panel - Intelligence Feed */}
        <div className="flex-1 border-r border-gray-700/50 p-6 flex flex-col overflow-hidden">
          <IntelligenceFeed items={summaryItems} />
        </div>

        {/* Center Divider */}
        <div className="w-px bg-gradient-to-b from-transparent via-sovereign-blue/50 to-transparent" />

        {/* Right Panel - Dialpad & Sovereignty */}
        <div className="w-80 p-6 flex flex-col overflow-hidden">
          <GlassmorphismDialpad
            onCallStart={handleCallStart}
            onCallEnd={handleCallEnd}
            isCallActive={isCallActive}
            isLoading={isLoading}
          />

          {/* Sovereignty Meter at Bottom */}
          <div className="mt-6">
            <SovereigntyMeter
              isProcessing={isProcessing}
              isWipingMemory={isWipingMemory}
              dataPointsStored={dataPointsStored}
            />
          </div>
        </div>
      </div>

      {/* Audio Player for streaming chunks */}
      <AudioPlayer audioChunks={audioChunks} isPlaying={isProcessing} />
    </>
  );
}
