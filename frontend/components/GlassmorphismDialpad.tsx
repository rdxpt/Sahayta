import React, { useState } from 'react';
import { WaveformVisualizer } from './WaveformVisualizer';

interface DialpadProps {
  onCallStart: () => void;
  onCallEnd: () => void;
  isCallActive: boolean;
  isLoading: boolean;
}

export const GlassmorphismDialpad: React.FC<DialpadProps> = ({
  onCallStart,
  onCallEnd,
  isCallActive,
  isLoading,
}) => {
  const [hoveredButton, setHoveredButton] = useState<string | null>(null);
  const [dialedNumber, setDialedNumber] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const dialpadNumbers = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#'],
  ];

  const handleNumberClick = (num: string) => {
    if (dialedNumber.length < 10) {
      setDialedNumber((prev) => prev + num);
      setErrorMsg(null);
    }
  };

  const handleDelete = () => {
    setDialedNumber((prev) => prev.slice(0, -1));
    setErrorMsg(null);
  };

  const handleDialClick = () => {
    if (isCallActive) {
      onCallEnd();
      setDialedNumber('');
    } else {
      if (dialedNumber === '311') {
        onCallStart();
      } else {
        setErrorMsg('Dial 311 Only');
        // Visual shake effect could go here
      }
    }
  };

  const handleSimulateIncoming = () => {
    if (isCallActive) return;
    setDialedNumber('Incoming...');
    setTimeout(() => {
        onCallStart();
    }, 500);
  };

  return (
    <div className="flex flex-col h-full justify-between relative">
      {/* Header */}
      <div className="pb-4">
        <h1 className="text-2xl font-bold text-sovereign-blue mb-1">MCD 311</h1>
        <p className="text-xs text-gray-400 uppercase tracking-widest">Grievance Redressal</p>
        <div className="mt-3 h-1 bg-gradient-to-r from-sovereign-green via-sovereign-blue to-sovereign-purple rounded-full opacity-50" />
      </div>

      {/* Number Display Screen with Delete */}
      <div className="glassmorphism-inner bg-black/40 p-4 rounded-lg mb-4 flex items-center justify-between border border-sovereign-blue/30 shadow-inner min-h-[70px]">
        <div className="flex-grow text-right pr-3 overflow-hidden">
             <span className={`text-3xl font-mono tracking-widest ${errorMsg ? 'text-red-500' : (isCallActive ? 'text-green-400' : 'text-sovereign-blue')}`}>
              {errorMsg || dialedNumber || (isCallActive ? 'CONNECTED' : '')}
              {!isCallActive && !errorMsg && <span className="animate-pulse ml-1 text-sovereign-green">_</span>}
            </span>
        </div>
        {/* Delete Button */}
        <button 
           onClick={handleDelete}
           disabled={isCallActive}
           className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-white/10 text-gray-400 hover:text-red-400 transition-colors"
        >
          ⌫
        </button>
      </div>

      {/* Waveform Visualizer */}
      <div className="glassmorphism-sm p-3 rounded-lg mb-4 h-16 relative overflow-hidden">
         {/* Live Indicator overlay */}
         <div className="absolute top-1 right-2 z-10">
            <div className={`w-2 h-2 rounded-full ${isCallActive ? 'bg-red-500 animate-ping' : 'bg-green-500/50'}`}></div>
         </div>
        <WaveformVisualizer isActive={isCallActive} />
      </div>

      {/* Center: Simulate Receive Call Button */}
      <div className="flex justify-center mb-6">
        <button
          onClick={handleSimulateIncoming}
          disabled={isLoading || isCallActive}
          className={`group relative w-24 h-24 rounded-full font-bold text-xs uppercase tracking-wider transition-all duration-300 ${
            isCallActive 
              ? 'bg-gray-700 opacity-50 cursor-not-allowed'
              : 'bg-gradient-to-br from-indigo-600 to-purple-700 hover:scale-110 shadow-lg hover:shadow-indigo-500/50'
          }`}
        >
          <div className="flex flex-col items-center justify-center h-full">
            <span className="text-2xl mb-1">📲</span>
            <span className="text-[10px] leading-tight opacity-80 group-hover:opacity-100">Simulate<br/>Inbound</span>
          </div>
          {!isCallActive && (
              <div className="absolute inset-0 rounded-full border border-indigo-500/30 animate-ping-slow" />
          )}
        </button>
      </div>

      {/* Status Text */}
      <div className="text-center mb-4">
        <p className="text-sm font-mono">
          {isCallActive ? (
            <span className="text-sovereign-green animate-pulse">● CALL IN PROGRESS</span>
          ) : (
            <span className="text-gray-400">System Ready</span>
          )}
        </p>
      </div>

      {/* Dialpad Grid */}
      <div className="grid grid-cols-3 gap-3 mb-6">
        {dialpadNumbers.map((row, rowIdx) =>
          row.map((num) => (
            <button
              key={num}
              onClick={() => handleNumberClick(num)}
              onMouseEnter={() => setHoveredButton(num)}
              onMouseLeave={() => setHoveredButton(null)}
              disabled={isCallActive || isLoading}
              className={`aspect-square rounded-full font-bold text-lg transition-all duration-200 active:scale-95 ${
                hoveredButton === num
                  ? 'glassmorphism bg-sovereign-blue/30 text-sovereign-blue scale-110 glow-blue'
                  : 'glassmorphism hover:bg-sovereign-blue/20 text-gray-300'
              } ${isCallActive || isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
            >
              {num}
            </button>
          ))
        )}
      </div>

      {/* Call Button (Replaces Emergency) */}
      <button 
        onClick={handleDialClick}
        disabled={isLoading}
        className={`w-full py-4 font-bold text-lg rounded-full transition-all duration-200 uppercase tracking-wider shadow-lg hover:shadow-xl flex items-center justify-center gap-2 ${
            isCallActive 
             ? 'bg-red-600 hover:bg-red-700 text-white'
             : 'bg-green-600 hover:bg-green-700 text-white'
        }`}
      >
        <span>{isCallActive ? 'End Call' : 'Call 311'}</span>
        <span className="text-xl">{isCallActive ? '📞' : '☎️'}</span>
      </button>
    </div>
  );
};
