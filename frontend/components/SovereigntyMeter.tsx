import React, { useState, useEffect } from 'react';

interface SovereigntyMeterProps {
  isProcessing: boolean;
  isWipingMemory: boolean;
  dataPointsStored: number;
}

export const SovereigntyMeter: React.FC<SovereigntyMeterProps> = ({
  isProcessing,
  isWipingMemory,
  dataPointsStored,
}) => {
  const [glowIntensity, setGlowIntensity] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setGlowIntensity((prev) => (prev + 1) % 100);
    }, 50);
    return () => clearInterval(interval);
  }, []);

  const getStatus = () => {
    if (isWipingMemory) return { text: '🗑️ WIPING', color: 'text-sovereign-green', glow: true };
    if (isProcessing) return { text: '🔐 PROCESSING', color: 'text-sovereign-blue', glow: true };
    return { text: '✓ SOVEREIGN', color: 'text-sovereign-green', glow: false };
  };

  const status = getStatus();
  const glowClass = status.glow ? 'animate-glow' : '';

  return (
    <div className="glassmorphism-sm p-4 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-xs font-mono text-gray-400 uppercase">Data Sovereignty</span>
        <span className={`text-sm font-bold ${status.color} ${glowClass}`}>
          {status.text}
        </span>
      </div>

      {/* Status Indicator */}
      <div className="flex items-center gap-2">
        <div
          className={`w-3 h-3 rounded-full ${
            isWipingMemory
              ? 'animate-pulse bg-sovereign-green'
              : isProcessing
              ? 'animate-pulse bg-sovereign-blue'
              : 'bg-sovereign-green'
          }`}
        />
        <span className="text-xs text-gray-300">
          {isWipingMemory ? 'Memory deletion in progress' : isProcessing ? 'Processing locally' : 'Zero persistence mode'}
        </span>
      </div>

      {/* Data Points Counter */}
      <div className="flex justify-between items-center bg-sovereign-dark/50 rounded-lg p-2">
        <span className="text-xs text-gray-400">Stored Data Points</span>
        <span className="text-sm font-mono text-sovereign-green">{dataPointsStored}</span>
      </div>

      {/* Progress Bar (appears during wipe) */}
      {isWipingMemory && (
        <div className="w-full bg-sovereign-dark/50 rounded-full h-1.5 overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-sovereign-green to-sovereign-blue animate-pulse"
            style={{ width: `${(glowIntensity / 100) * 100}%` }}
          />
        </div>
      )}
    </div>
  );
};
