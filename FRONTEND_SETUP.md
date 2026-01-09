# MCD 311 Sovereign Voice AI - Complete Setup Guide

**Frontend + Backend Integration for Hack4Delhi 2026**

---

## 🎯 What You Have

✅ **Python Backend:** Complete LLM + FSM + Memory system  
✅ **Frontend:** Next.js with Glassmorphism UI  
✅ **WebSocket Server:** Real-time streaming integration  
✅ **Demo Scripts:** Working demos showing the system in action  

---

## 🚀 5-Minute Quick Start

### Step 1: Start Redis Server
```powershell
"C:\Program Files\Redis\redis-server.exe"
# Leave running in background
```

### Step 2: Start Ollama (if you want real LLM)
```powershell
ollama serve
# Leave running in background
# Models will load when needed
```

### Step 3: Terminal 1 - Start WebSocket Server
```powershell
cd C:\Users\rdxpt\cooks\pyML\Sahayta
python websocket_server_integrated.py
# Shows: "WebSocket available at: ws://localhost:8000/ws/call"
```

### Step 4: Terminal 2 - Start Frontend
```powershell
cd C:\Users\rdxpt\cooks\pyML\Sahayta\frontend
npm install  # (first time only)
npm run dev
# Shows: "Ready at http://localhost:3000"
```

### Step 5: Open Browser
Visit: **http://localhost:3000**

Click the green **☎️** button and watch the magic happen.

---

## 📋 System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                 Browser (Next.js: 3000)                      │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────┐  ┌─────────────────────────┐   │
│  │ Intelligence Feed       │  │ Glassmorphism Dialpad   │   │
│  │ (Text Chunks)           │  │ + Sovereignty Meter     │   │
│  │ • Intent                │  │ + Waveform Viz          │   │
│  │ • Entity                │  │                         │   │
│  │ • Action                │  │ [CALL BUTTON]          │   │
│  └─────────────────────────┘  └─────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
         ↕ WebSocket (Bidirectional)
┌──────────────────────────────────────────────────────────────┐
│       FastAPI Server (8000) - websocket_server_integrated.py │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌─────────────┐  ┌──────────────────┐  │
│  │ LLM Engine     │  │ Memory Mgr  │  │ FSM Workflow     │  │
│  │ (Ollama)       │  │ (Redis)     │  │ (7-node graph)   │  │
│  └────────────────┘  └─────────────┘  └──────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎬 The Hack4Delhi Demo Flow

### **1. Judge Sees (0:00)**
- Professional UI with dialpad and intelligence feed
- "Ready to receive call" status
- Sovereignty meter showing "✓ SOVEREIGN"

### **2. Click Call Button (0:02)**
- Glassmorphism dialpad lights up
- Waveform visualizer starts animating
- Status changes to "● CALL ACTIVE"

### **3. Text Streaming (0:03-0:08)**
- Intelligence feed populates:
  - 🎯 Intent: "Grievance Registration"
  - 📍 Entity: "Amit Singh"
  - 📍 Location: "Lajpat Nagar, Delhi"
  - ⚡ Category: "STREET_LIGHT (0.97 confidence)"
  - ⚡ Priority: "HIGH - Safety hazard"
  - ⚡ Ticket: "MCD-2026-55823"

### **4. Data Storage Visualization (0:08)**
- Sovereignty meter shows: "Data Points: 6"
- Judge can see citizen data in system

### **5. Memory Wipe (0:10)**
- Status changes to: "🗑️ WIPING"
- Sovereignty meter shows progress bar
- Data Points count down: 6 → 5 → 4 → 3 → 2 → 1 → 0
- Judge watches data disappear in real-time

### **6. Verification (0:15)**
- Status: "✓ SOVEREIGN"
- "All citizen data permanently deleted"
- "Call completed. Zero persistence confirmed."

**Total time: 15 seconds. Judge is amazed.** 🎯

---

## 📦 File Structure

```
Sahayta/
├── frontend/                          (Next.js project)
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── pages/
│   │   ├── index.tsx                  (Main page, WebSocket client)
│   │   ├── _document.tsx
│   │   └── api/health.ts
│   ├── components/
│   │   ├── GlassmorphismDialpad.tsx
│   │   ├── IntelligenceFeed.tsx
│   │   ├── SovereigntyMeter.tsx
│   │   ├── WaveformVisualizer.tsx
│   │   ├── AudioPlayer.tsx
│   │   └── Logo.tsx
│   ├── styles/
│   │   └── globals.css                (Tailwind + custom)
│   └── README.md
│
├── src/                               (Python modules)
│   ├── agent_state.py
│   ├── memory_manager.py
│   ├── llm_integration.py
│   ├── workflow.py
│   └── ...
│
├── config/
│   └── settings.py                    (Config)
│
├── websocket_server.py                (Simple mock server)
├── websocket_server_integrated.py     (Real backend integration)
├── demo_real.py                       (Working demo with Redis)
├── watch_and_demo.py                  (Auto-launcher)
└── ...
```

---

## 🔧 Configuration

### **Frontend Config**
File: `frontend/pages/index.tsx`

```typescript
// Default WebSocket URL (change if needed)
const wsUrl = `${wsProtocol}//localhost:8000/ws/call`;
```

### **Backend Config**
File: `config/settings.py`

```python
# Redis configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_TTL = 10  # seconds

# Ollama configuration
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODELS = ["mistral", "neural-chat"]
```

### **WebSocket Server Port**
File: `websocket_server_integrated.py`

```python
# Default: 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 🧪 Testing Checklist

| Test | Steps | Expected |
|------|-------|----------|
| **WebSocket Connection** | Open DevTools → Network → Click call | WS connection appears |
| **Text Streaming** | Click call → Wait | Text appears in feed (6 items) |
| **Data Count** | During call | Number increases: 0→6 |
| **Memory Wipe** | Wait for auto-complete | Count: 6→5→4→3→2→1→0 |
| **Sovereignty Status** | Observe meter | Changes: PROCESSING → WIPING → SOVEREIGN |
| **Waveform** | Listen/watch | Bars animate during call |
| **Call Complete** | After 15s | Connection closes automatically |

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Connection refused" on WebSocket** | Ensure `websocket_server_integrated.py` is running on port 8000 |
| **Blank intelligence feed** | Check browser console (F12) for JS errors |
| **No data count increase** | Verify Redis is running (`redis-cli ping` should return PONG) |
| **Waveform not animating** | Wait for LLM models to load, or re-click call button |
| **"Ollama not available" message** | Optional - system still works without LLM (uses mocks) |
| **Port 3000 already in use** | Change `npm run dev` to use different port: `npm run dev -- -p 3001` |
| **Port 8000 already in use** | Change WebSocket server port in both files and update frontend URL |

---

## 🎓 For IAS Officers (Judges)

### What You're Seeing

**This is NOT traditional cloud processing:**

1. ✅ **No API calls to cloud** - All processing happens locally
2. ✅ **No persistent storage** - Data deleted immediately after call
3. ✅ **Real LLM inference** - Using Ollama (open-source, runs locally)
4. ✅ **Transparent audit trail** - You watch data appear and disappear

### Why This Matters for Delhi

- **Data Sovereignty:** Delhi govt controls all data (no vendor lock-in)
- **Cost Efficient:** Open-source LLM (no per-API-call charges)
- **Security:** No internet required (can run offline)
- **Compliance:** GDPR "Right to be Forgotten" implemented by design

### The Key Innovation

**Typical AI system:**
```
Citizen → Upload to Cloud → Wait 3-5s → Get Response
        → Data stays in cloud for 30+ days
```

**MCD 311 Sovereign System:**
```
Citizen → Local LLM (instant) → Memory Wipe (automatic)
        → Zero data persistence
```

---

## 📞 Quick Commands

### **Start All Services (4 terminals)**

**Terminal 1:**
```powershell
"C:\Program Files\Redis\redis-server.exe"
```

**Terminal 2:**
```powershell
ollama serve
```

**Terminal 3:**
```powershell
cd C:\Users\rdxpt\cooks\pyML\Sahayta
python websocket_server_integrated.py
```

**Terminal 4:**
```powershell
cd C:\Users\rdxpt\cooks\pyML\Sahayta\frontend
npm run dev
```

**Browser:**
```
http://localhost:3000
```

---

## 🎯 Success Metrics

When judges evaluate your system:

- [ ] UI loads smoothly (no console errors)
- [ ] Click call button → System responds within 2 seconds
- [ ] Text appears chunk-by-chunk (not all at once)
- [ ] Sovereignty meter shows "PROCESSING" with blue glow
- [ ] Data count goes from 0→6
- [ ] Memory wipe shows progress bar
- [ ] Data count goes from 6→0 within 5 seconds
- [ ] Final status: "✓ SOVEREIGN"
- [ ] Call completes without errors

**If all checks pass: You've won Hack4Delhi.** 🏆

---

## 🚀 Advanced: Production Deployment

### **Option 1: Docker Compose**
```bash
docker-compose up
# Starts: Frontend, WebSocket, Redis, Ollama
```

### **Option 2: Cloud Deployment (Azure)**
```bash
azd up
# Deploys to Azure Container Instances
# Keeps data local (App Service → Memory only)
```

### **Option 3: Manual Deployment**
```bash
# Frontend: Vercel, Netlify
# Backend: AWS EC2, Azure VM, GCP
# LLM: Local Ollama on same machine
```

---

## 📝 Notes for Judges

**During presentation, emphasize:**

1. **"This is 100% local processing"** - Point to localhost URLs
2. **"Watch the memory wipe in real-time"** - Show data count: 6→0
3. **"This runs offline"** - No internet dependency (except initial setup)
4. **"Production-grade UI"** - Government-style glassmorphism design
5. **"Real innovation"** - FSM + Instant Memory Wipe (not just LLM)

---

## 🎊 You're Ready!

You have everything needed to win Hack4Delhi:

✅ Working demo  
✅ Real backend integration  
✅ Professional UI  
✅ Data sovereignty visualization  
✅ Complete documentation  

**Let's show those judges what data sovereignty really means!** 🎯🚀

---

**Questions?** Check the README files in each directory:
- `frontend/README.md` - Frontend details
- `ARCHITECTURE.md` - System design
- `QUICKSTART.md` - Quick reference

**Good luck! You've got this!** 🌟
