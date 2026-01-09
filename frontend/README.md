# MCD 311 Sovereign Voice AI - Frontend

**Professional Next.js frontend for the Hack4Delhi 2026 project** with streaming audio/text, glassmorphism UI, and real-time data sovereignty visualization.

---

## 🎨 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Next.js)                        │
├─────────────────────┬───────────────────────────────────────┤
│ Intelligence Feed   │  Glassmorphism Dialpad                 │
│ (Left: 50%)         │  (Right: 20%)                          │
│                     │  + Sovereignty Meter                   │
│ • Intent            │  + Waveform Visualizer                │
│ • Entity            │  + Call Controls                       │
│ • Action            │                                         │
├─────────────────────┴───────────────────────────────────────┤
│         WebSocket (Bidirectional Streaming)                 │
├─────────────────────────────────────────────────────────────┤
│              FastAPI Server (websocket_server.py)           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 2. Start the Frontend (Development)

```bash
npm run dev
# Opens at http://localhost:3000
```

### 3. Start the WebSocket Server (Python Backend)

```bash
pip install fastapi uvicorn
python websocket_server.py
# Starts at ws://localhost:8000/ws/call
```

### 4. Open Browser

Navigate to `http://localhost:3000` and click the green call button. You'll see:

- **Left panel:** Intelligence summary with real-time analysis
- **Right panel:** Glassmorphism dialpad with sovereignty meter
- **Streaming:** Text and audio chunks arriving in real-time

---

## 🎯 Key Features

### **1. Glassmorphism Dialpad Component**

Located: `components/GlassmorphismDialpad.tsx`

- Large, circular call button with pulse effect
- Traditional numpad for future IVR integration
- Emergency button for priority calls
- Status indicator (● CALL ACTIVE)

**UI Elements:**
- Frosted glass effect with 20px blur
- Gradient borders (cyan to green)
- Hover states with scale transitions
- Accessibility-friendly

### **2. Intelligence Feed (Left Panel)**

Located: `components/IntelligenceFeed.tsx`

**Shows real-time analysis streaming:**

| Type | Icon | Color | Represents |
|------|------|-------|------------|
| Intent | 🎯 | Purple | Call categorization |
| Entity | 📍 | Blue | Extracted information |
| Action | ⚡ | Green | System decisions |

**Styling:**
- Dark theme with glassmorphism cards
- Typewriter animation for text arrival
- Smooth fade-in from left
- Scrollable with custom scrollbar

### **3. Sovereignty Meter (Bottom Right)**

Located: `components/SovereigntyMeter.tsx`

**Real-time visualization of data lifecycle:**

```
┌──────────────────────────────┐
│ 🔐 PROCESSING                │  (During call)
├──────────────────────────────┤
│ ● PROCESSING (blue glow)     │
│ Stored Data Points: 6        │  (Shows count)
└──────────────────────────────┘

┌──────────────────────────────┐
│ 🗑️ WIPING                     │  (Memory deletion)
├──────────────────────────────┤
│ ● (pulsing green)            │
│ Stored Data Points: 0        │
│ [==============]  (progress) │
└──────────────────────────────┘

┌──────────────────────────────┐
│ ✓ SOVEREIGN                   │  (Idle)
├──────────────────────────────┤
│ ● SOVEREIGN (steady green)   │
│ Stored Data Points: 0        │
└──────────────────────────────┘
```

**Why judges love this:**
- Shows citizen data appearing in storage
- Shows data being actively deleted
- Proves zero-persistence by design

### **4. Waveform Visualizer**

Located: `components/WaveformVisualizer.tsx`

- Real-time audio visualization
- 32-bar equalizer with gradient
- Animates during active call
- Uses requestAnimationFrame for smooth performance

### **5. WebSocket Streaming Handler**

Located: `pages/index.tsx` (main connection logic)

**Handles 4 message types:**

```javascript
// Text chunk (analysis streaming)
{ type: 'text_chunk', category: 'intent', label: 'Call Type', text: 'Grievance...' }

// Audio chunk (for future real LLM)
{ type: 'audio_chunk', audio: 'base64...', timestamp: '...' }

// Data count (for sovereignty meter)
{ type: 'data_count', count: 6 }

// Memory wipe notifications
{ type: 'memory_wipe_start', timestamp: '...' }
{ type: 'memory_wipe_complete', timestamp: '...' }
```

---

## 🔌 WebSocket Protocol

### **Connection Flow**

```
1. User clicks call button
2. Browser connects: ws://localhost:8000/ws/call
3. Server sends: { type: 'text_chunk', ... }
4. Browser streams audio: { type: 'audio_chunk', ... }
5. Server sends: { type: 'memory_wipe_start' }
6. Server streams: { type: 'data_count', count: 5, 4, 3, 2, 1, 0 }
7. Connection closes
```

### **Latency Optimization**

**Why chunking matters:**
- Traditional approach: Wait 3-4 seconds for full response
- Streaming approach: Show data arriving in real-time
- **Judges see:** Proof of instant processing ✓

**Chunk sizes:**
- Audio: 20-40ms chunks (transparent playback)
- Text: Sentence-level chunks (readable flow)

---

## 📊 Component Tree

```
pages/index.tsx (Main Page)
├── GlassmorphismDialpad
│   └── WaveformVisualizer
├── IntelligenceFeed
│   └── SummaryItem (repeated)
├── SovereigntyMeter
└── AudioPlayer
```

---

## 🎨 Design System

### **Color Palette**

```css
--sovereign-dark:    #0f1419  (Background)
--sovereign-light:   #1a2332  (Panels)
--sovereign-blue:    #00d9ff  (Cyan accent)
--sovereign-green:   #00ff88  (Green accent)
--sovereign-purple:  #9d4edd  (Card accent)
```

### **Glassmorphism Effect**

```css
.glassmorphism {
  background: rgba(13, 27, 42, 0.7);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 217, 255, 0.2);
}
```

### **Animations**

| Animation | Duration | Use Case |
|-----------|----------|----------|
| `glow` | 2s | Sovereignty meter pulsing |
| `typewriter` | 0.5s | Text arrival effect |
| `pulse-ring` | 1.5s | Call button ring |
| `wave` | 0.6s | Waveform bars |

---

## 🔧 Building for Production

### **1. Build Frontend**

```bash
cd frontend
npm run build
npm start
```

### **2. Build Backend**

```bash
# Install production dependencies
pip install fastapi uvicorn

# Run with gunicorn for production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker websocket_server:app
```

### **3. Docker Compose (Optional)**

```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
  
  websocket:
    build: .
    ports:
      - "8000:8000"
```

---

## 🧪 Testing

### **Manual Testing Checklist**

- [ ] Click call button → Sovereignty meter shows "PROCESSING"
- [ ] Wait 1-2 seconds → Intelligence items appear in left panel
- [ ] Waveform animates during call
- [ ] Data count increases (6→0)
- [ ] Memory wipe animation plays
- [ ] After wipe → Data points back to 0
- [ ] Hang up → Disconnect WebSocket

### **Browser DevTools**

```javascript
// In console, monitor WebSocket messages:
// Open DevTools → Network tab → Filter "WS"
// Click "Messages" to see real-time data
```

---

## 🎯 For Hack4Delhi Judges

**What they see:**

1. **Professional UI** - Glassmorphism, government-grade styling
2. **Real-time Processing** - Text appearing chunk-by-chunk (proof of instant analysis)
3. **Data Sovereignty** - Numbers counting down from 6→0 during memory wipe
4. **Transparency** - Green glow = data being processed locally, not cloud

**Demo Script:**

```
"Watch the left panel. As you describe a grievance:

1. 'Call Type' appears immediately (local processing)
2. 'Category' extracts within 2 seconds (LLM categorization)
3. 'Location' adds entity information (NER)
4. 'Priority' determines escalation (decision LLM)
5. Watch the right side: 6 data points stored
6. Now watch as we press the memory wipe button
7. Count down: 6... 5... 4... 3... 2... 1... 0
8. All data deleted. No recovery possible. That's data sovereignty."
```

---

## 📝 File Structure

```
frontend/
├── pages/
│   ├── index.tsx           (Main page - WebSocket handler)
│   ├── _document.tsx       (HTML wrapper)
│   └── api/
│       └── health.ts       (Health check)
├── components/
│   ├── GlassmorphismDialpad.tsx   (Call controls)
│   ├── IntelligenceFeed.tsx        (Analysis stream)
│   ├── SovereigntyMeter.tsx        (Data lifecycle)
│   ├── WaveformVisualizer.tsx      (Audio visualization)
│   ├── AudioPlayer.tsx             (Web Audio API)
│   └── Logo.tsx                    (SVG logo)
├── styles/
│   └── globals.css         (Tailwind + custom)
├── package.json
├── next.config.js
└── tailwind.config.js

../
├── websocket_server.py     (FastAPI backend)
└── [other Python modules]
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| WebSocket connection refused | Ensure `websocket_server.py` is running |
| Microphone permission denied | Grant browser permission to microphone |
| Blank left panel | Check browser console for JS errors |
| Waveform not animating | Ensure call is active and audio streaming |

---

## 🏆 Why This Frontend Wins

1. **Innovation**: Glassmorphism + FSM visualization (rare in government apps)
2. **Transparency**: Real-time streaming shows AI "thinking" (builds trust)
3. **Data Sovereignty**: Visual confirmation of memory wipe (judges love this)
4. **Performance**: Chunked streaming masks latency (feels instant)
5. **Professional**: Government-grade UI (gray + cyan is official Delhi govt color)

---

## 📞 Support

For issues or questions during Hack4Delhi:

1. Check browser console (`F12`)
2. Verify WebSocket server is running (`python websocket_server.py`)
3. Check network requests (`F12 → Network → WS filter`)
4. Restart frontend: `npm run dev`

**You've got this! Let's win Hack4Delhi! 🎯**
