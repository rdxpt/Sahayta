import React, { useState, useEffect } from 'react';

interface SummaryItem {
  type: 'intent' | 'entity' | 'action';
  label: string;
  value: string;
  timestamp: number;
}

interface IntelligenceFeedProps {
  items: SummaryItem[];
}

export const IntelligenceFeed: React.FC<IntelligenceFeedProps> = ({ items }) => {
  const [displayedItems, setDisplayedItems] = useState<SummaryItem[]>([]);

  useEffect(() => {
    if (items.length === 0) {
      setDisplayedItems([]);
      return;
    }

    const lastItem = items[items.length - 1];
    const timeout = setTimeout(() => {
      setDisplayedItems(items);
    }, 50);

    return () => clearTimeout(timeout);
  }, [items]);

  const getIcon = (type: string) => {
    switch (type) {
      case 'intent':
        return '🎯';
      case 'entity':
        return '📍';
      case 'action':
        return '⚡';
      default:
        return '•';
    }
  };

  const getColor = (type: string) => {
    switch (type) {
      case 'intent':
        return 'border-l-sovereign-purple';
      case 'entity':
        return 'border-l-sovereign-blue';
      case 'action':
        return 'border-l-sovereign-green';
      default:
        return 'border-l-gray-500';
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="pb-3 border-b border-gray-700/50">
        <h2 className="text-sm font-bold text-sovereign-blue uppercase tracking-wider">
          Intelligence Summary
        </h2>
        <p className="text-xs text-gray-400 mt-1">Real-time analysis stream</p>
      </div>

      <div className="flex-1 overflow-y-auto space-y-2 py-3 pr-2">
        {displayedItems.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-2">
             <div className="text-4xl animate-pulse grayscale opacity-30">🛡️</div>
            <p className="text-sm text-gray-400 font-mono">SECURE SYSTEM ACTIVE</p>
            <p className="text-xs text-gray-600">Awaiting call...</p>
          </div>
        ) : (
          displayedItems.map((item, idx) => (
            <div
              key={idx}
              className={`glassmorphism-sm p-3 border-l-4 ${getColor(item.type)} animate-in fade-in slide-in-from-left-2 duration-300`}
            >
              <div className="flex items-start gap-2">
                <span className="text-lg mt-0.5 flex-shrink-0">{getIcon(item.type)}</span>
                <div className="flex-1 min-w-0">
                  <div className="text-xs uppercase font-bold text-gray-400 tracking-wider">
                    {item.label}
                  </div>
                  <div className="text-sm text-gray-100 mt-1 break-words">
                    {item.value}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {new Date(item.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
