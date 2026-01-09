import React, { useEffect, useState } from 'react';

interface GrievanceData {
  ticketId: string;
  issueCategory: string;
  location: string;
  timestamp: string;
  citizenName?: string;
  status: 'active' | 'wiped';
}

interface LiveGrievanceReportProps {
  websocketData: any[];
  isCallActive: boolean;
}

export const LiveGrievanceReport: React.FC<LiveGrievanceReportProps> = ({
  websocketData,
  isCallActive,
}) => {
  const [grievanceData, setGrievanceData] = useState<GrievanceData>({
    ticketId: '',
    issueCategory: '',
    location: '',
    timestamp: '',
    citizenName: '',
    status: 'active',
  });

  const [showWipeAnimation, setShowWipeAnimation] = useState(false);

  useEffect(() => {
    // Parse websocket data to extract entities
    websocketData.forEach((item) => {
      if (item.type === 'text_chunk') {
        switch (item.category) {
          case 'entity':
            if (item.label === 'Citizen') {
              setGrievanceData((prev) => ({ ...prev, citizenName: item.text }));
            } else if (item.label === 'Location') {
              setGrievanceData((prev) => ({ ...prev, location: item.text }));
            }
            break;
          case 'action':
            if (item.label === 'Category') {
              setGrievanceData((prev) => ({ ...prev, issueCategory: item.text }));
            } else if (item.label === 'Ticket Created') {
              setGrievanceData((prev) => ({
                ...prev,
                ticketId: item.text,
                timestamp: new Date().toLocaleString(),
              }));
            }
            break;
        }
      }

      // Detect memory wipe
      if (item.type === 'memory_wipe_complete') {
        setShowWipeAnimation(true);
        setTimeout(() => {
          setGrievanceData({
            ticketId: '',
            issueCategory: '',
            location: '',
            timestamp: '',
            citizenName: '',
            status: 'wiped',
          });
        }, 1500);
      }
    });
  }, [websocketData]);

  // Reset on new call
  useEffect(() => {
    if (isCallActive && grievanceData.status === 'wiped') {
      setGrievanceData({
        ticketId: '',
        issueCategory: '',
        location: '',
        timestamp: '',
        citizenName: '',
        status: 'active',
      });
      setShowWipeAnimation(false);
    }
  }, [isCallActive]);

  return (
    <div className="glassmorphism p-6 rounded-lg relative overflow-hidden min-h-[400px]">
      {/* Header */}
      <div className="mb-6 border-b border-sovereign-blue/30 pb-3">
        <h2 className="text-xl font-bold text-sovereign-blue flex items-center gap-2">
          <span className="text-2xl">📋</span>
          Live Grievance Report
        </h2>
        <p className="text-xs text-gray-400 mt-1">Real-time ticket generation</p>
      </div>

      {/* Report Fields */}
      <div className="space-y-4">
        {/* Ticket ID */}
        <div className="glassmorphism-inner p-3 rounded-lg">
          <label className="text-xs text-gray-400 uppercase tracking-wider block mb-1">
            Ticket ID
          </label>
          <p className="text-lg font-mono text-sovereign-green">
            {grievanceData.ticketId || (
              <span className="text-gray-500 animate-pulse">Pending...</span>
            )}
          </p>
        </div>

        {/* Issue Category */}
        <div className="glassmorphism-inner p-3 rounded-lg">
          <label className="text-xs text-gray-400 uppercase tracking-wider block mb-1">
            Issue Category
          </label>
          <p className="text-lg font-semibold text-white">
            {grievanceData.issueCategory || (
              <span className="text-gray-500 animate-pulse">Analyzing...</span>
            )}
          </p>
        </div>

        {/* Ward/Location */}
        <div className="glassmorphism-inner p-3 rounded-lg">
          <label className="text-xs text-gray-400 uppercase tracking-wider block mb-1">
            Ward / Location
          </label>
          <p className="text-lg text-white">
            {grievanceData.location || (
              <span className="text-gray-500 animate-pulse">Extracting...</span>
            )}
          </p>
        </div>

        {/* Citizen Name */}
        {grievanceData.citizenName && (
          <div className="glassmorphism-inner p-3 rounded-lg">
            <label className="text-xs text-gray-400 uppercase tracking-wider block mb-1">
              Reported By
            </label>
            <p className="text-lg text-white">{grievanceData.citizenName}</p>
          </div>
        )}

        {/* Timestamp */}
        <div className="glassmorphism-inner p-3 rounded-lg">
          <label className="text-xs text-gray-400 uppercase tracking-wider block mb-1">
            Timestamp
          </label>
          <p className="text-sm font-mono text-gray-300">
            {grievanceData.timestamp || (
              <span className="text-gray-500">--:--:--</span>
            )}
          </p>
        </div>
      </div>

      {/* Data Wiped Overlay */}
      {showWipeAnimation && (
        <div className="absolute inset-0 bg-black/90 flex items-center justify-center backdrop-blur-sm animate-fade-in z-50">
          <div className="text-center">
            <div className="text-6xl mb-4 animate-pulse">🔒</div>
            <h3 className="text-4xl font-bold text-red-500 tracking-widest transform rotate-[-5deg] border-4 border-red-500 px-8 py-4 bg-black/80">
              DATA WIPED
            </h3>
            <p className="text-sm text-gray-400 mt-4">
              All citizen data permanently deleted
            </p>
          </div>
        </div>
      )}

      {/* Status Indicator */}
      <div className="mt-6 pt-4 border-t border-sovereign-blue/20">
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-400">Data Sovereignty:</span>
          <span className="flex items-center gap-2">
            <div
              className={`w-2 h-2 rounded-full ${
                grievanceData.status === 'active' ? 'bg-green-500 animate-pulse' : 'bg-gray-500'
              }`}
            ></div>
            <span className="text-sovereign-green font-mono">
              {grievanceData.status === 'active' ? 'EPHEMERAL MODE' : 'CLEARED'}
            </span>
          </span>
        </div>
      </div>
    </div>
  );
};
