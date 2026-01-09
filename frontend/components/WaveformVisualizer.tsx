import React, { useState, useEffect, useRef } from 'react';

interface WaveformProps {
  isActive: boolean;
}

export const WaveformVisualizer: React.FC<WaveformProps> = ({ isActive }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const [bars, setBars] = useState<number[]>(Array(32).fill(0));

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (isActive) {
        setBars((prev) =>
          prev.map(() => Math.random() * 0.8 + 0.2)
        );
      } else {
        // Idle Animation (Gentle Wave)
        const time = Date.now() / 300;
        setBars((prev) =>
          prev.map((_, i) => Math.sin(time + i * 0.5) * 0.15 + 0.2)
        );
      }

      bars.forEach((height, index) => {
        const x = (index / bars.length) * canvas.width;
        const barHeight = height * canvas.height * 0.8;
        const y = (canvas.height - barHeight) / 2;

        // Gradient
        const gradient = ctx.createLinearGradient(0, y, 0, y + barHeight);
        gradient.addColorStop(0, '#00ff88');
        gradient.addColorStop(1, '#00d9ff');

        ctx.fillStyle = gradient;
        ctx.fillRect(x + 2, y, canvas.width / 32 - 4, barHeight);
      });

      animationRef.current = requestAnimationFrame(draw);
    };

    animationRef.current = requestAnimationFrame(draw);

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isActive, bars]);

  return (
    <canvas
      ref={canvasRef}
      width={300}
      height={60}
      className="w-full h-16 opacity-80"
    />
  );
};
