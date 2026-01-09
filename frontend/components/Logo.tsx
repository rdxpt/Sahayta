import React from 'react';

export const Logo: React.FC = () => (
  <svg width="100%" height="100%" viewBox="0 0 200 200">
    <defs>
      <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style={{ stopColor: '#00ff88', stopOpacity: 1 }} />
        <stop offset="100%" style={{ stopColor: '#00d9ff', stopOpacity: 1 }} />
      </linearGradient>
    </defs>
    {/* Outer circle */}
    <circle cx="100" cy="100" r="95" fill="none" stroke="url(#grad1)" strokeWidth="2" opacity="0.5" />
    {/* Inner circle */}
    <circle cx="100" cy="100" r="80" fill="none" stroke="url(#grad1)" strokeWidth="1" opacity="0.3" />
    {/* Center dot */}
    <circle cx="100" cy="100" r="8" fill="url(#grad1)" />
  </svg>
);
