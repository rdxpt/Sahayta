# MCD 311 Frontend + Backend Integration Checklist

## ✅ Pre-Demo Verification

### System Services
- [ ] Redis running on port 6379
  ```powershell
  redis-cli ping
  # Expected: PONG
  ```

- [ ] Ollama running (optional for this demo)
  ```powershell
  ollama list
  # Can be empty - system handles gracefully
  ```

- [ ] WebSocket Server running on port 8000
  ```powershell
  curl http://localhost:8000/health
  # Expected: {"status": "healthy", ...}
  ```

- [ ] Frontend running on port 3000
  ```powershell
  curl http://localhost:3000
  # Expected: HTML page loads
  ```

---

## 🔧 Configuration Verification

### Frontend (pages/index.tsx)
```typescript
✓ WebSocket URL points to: ws://localhost:8000/ws/call
✓ Audio streaming enabled
✓ Data count updates working
✓ Memory wipe notifications enabled
```

### Backend (websocket_server_integrated.py)
```python
✓ Imports all Python modules correctly:
  - config.settings
  - src.memory_manager
  - src.llm_integration
  - src.workflow
  - src.agent_state

✓ Redis connection: localhost:6379
✓ Memory manager initialized
✓ LLM client initialized
✓ WebSocket endpoint: /ws/call on port 8000
```

### Python Environment
```bash
✓ All dependencies installed:
  pip list | grep -E "fastapi|uvicorn|redis|langchain"

✓ All Python modules present:
  - src/agent_state.py
  - src/memory_manager.py
  - src/llm_integration.py
  - src/workflow.py
  - config/settings.py
```

---

## 🚀 Quick Start Commands

### Terminal Setup (4 terminals needed)

**Terminal 1 - Redis:**
```powershell
"C:\Program Files\Redis\redis-server.exe"
# Wait for: "Ready to accept connections"
```

**Terminal 2 - Ollama (optional):**
```powershell
ollama serve
# Wait for: "listening on 127.0.0.1:11434"
```

**Terminal 3 - WebSocket Server:**
```powershell
cd C:\Users\rdxpt\cooks\pyML\Sahayta
python websocket_server_integrated.py
# Wait for: "Uvicorn running on http://0.0.0.0:8000"
```

**Terminal 4 - Frontend:**
```powershell
cd C:\Users\rdxpt\cooks\pyML\Sahayta\frontend
npm run dev
# Wait for: "Ready at http://localhost:3000"
```

**Browser:**
Open `http://localhost:3000`

---

## 🧪 Functional Tests

### Test 1: Page Loads
- [ ] Browser loads without errors (F12 console empty)
- [ ] Dialpad visible on right side
- [ ] Intelligence feed visible on left side
- [ ] Sovereignty meter visible at bottom right
- [ ] All text readable on dark background

### Test 2: Call Button Interaction
- [ ] Click green call button
- [ ] Button changes to red with "📞"
- [ ] Status shows "● CALL ACTIVE"
- [ ] Waveform starts animating (bars move)

### Test 3: Text Streaming
- [ ] Wait 5 seconds after clicking call
- [ ] Intelligence feed populates with 6 items:
  1. Intent: "Grievance Registration - Street Light Issue"
  2. Entity: "Citizen: Amit Singh"
  3. Entity: "Location: Lajpat Nagar, Delhi"
  4. Action: "Category: STREET_LIGHT (0.97)"
  5. Action: "Priority: HIGH - Safety hazard"
  6. Action: "Ticket: MCD-2026-55823"

### Test 4: Data Count Updates
- [ ] Sovereignty meter shows: "Stored Data Points: 0" initially
- [ ] After call starts, count increases to 6
- [ ] Each new text item increments the counter

### Test 5: Memory Wipe Animation
- [ ] After ~5 seconds, sovereignty meter changes to "🗑️ WIPING"
- [ ] Status color changes to green with animation
- [ ] Progress bar appears and fills
- [ ] Data count decrements: 6 → 5 → 4 → 3 → 2 → 1 → 0
- [ ] Each number takes ~0.15 seconds
- [ ] Takes ~1 second total for full wipe

### Test 6: Call Completion
- [ ] After wipe completes, status returns to "✓ SOVEREIGN"
- [ ] Intelligence feed shows: "✓ All citizen data permanently deleted"
- [ ] Intelligence feed shows: "Call completed. Zero persistence confirmed."
- [ ] Call automatically closes (or can be clicked to close)

### Test 7: Browser Console
- [ ] F12 → Console tab
- [ ] No red error messages
- [ ] No "Connection refused" errors
- [ ] Should see: "[WebSocket] Session XXXX connected"

### Test 8: Network Requests
- [ ] F12 → Network tab
- [ ] Click call button
- [ ] Should see WebSocket connection (filter by WS)
- [ ] Click on WebSocket → Messages tab
- [ ] Should see incoming messages with type: "text_chunk", "data_count", "memory_wipe_start", etc.

---

## 📊 Performance Checks

| Metric | Expected | Actual |
|--------|----------|--------|
| **Page Load Time** | < 2s | _____ |
| **Call Button Response** | < 500ms | _____ |
| **Text Appearance** | 1s intervals | _____ |
| **Memory Wipe Duration** | 1-2s | _____ |
| **Full Demo Duration** | 15-20s | _____ |

---

## 🔍 Debug Commands

### Check Redis Connection
```powershell
redis-cli
> PING
PONG
> KEYS *
(empty list or keys from previous runs)
```

### Check WebSocket Server Health
```powershell
curl http://localhost:8000/health
# Should return JSON with status: "healthy"
```

### Monitor WebSocket Messages
```javascript
// In browser console (F12):
// Open DevTools → Network → WS
// Click call button
// You should see messages flowing in real-time
```

### Check Python Imports
```powershell
python
>>> import sys
>>> sys.path.insert(0, 'C:\Users\rdxpt\cooks\pyML\Sahayta')
>>> from config.settings import Settings
>>> from src.memory_manager import MemoryManager
# Should import without errors
```

---

## 🎬 Demo Script (For Reference)

**[0:00]** Browser shows: http://localhost:3000  
**[0:05]** "This is MCD 311. Let me show you how data sovereignty works..."  
**[0:10]** Click green call button  
**[0:15]** "Watch the left side. Real-time intelligence stream..."  
**[0:20]** First item appears: "Grievance Registration"  
**[0:25]** More items appear: Citizen, Location, Category, Priority, Ticket  
**[0:45]** "Notice the right side. 6 data points stored in memory."  
**[1:00]** "Now, the innovation. No data persists. Watch:"  
**[1:05]** Data count starts decreasing: 6 → 5 → 4 → 3 → 2 → 1 → 0  
**[1:15]** Status shows: "✓ All citizen data permanently deleted"  
**[1:20]** "This is data sovereignty. That's our innovation."  

---

## ⚠️ Known Issues & Fixes

### Issue: "Cannot GET /"
**Cause:** Frontend not running  
**Fix:** Run `npm run dev` in frontend directory

### Issue: WebSocket: ECONNREFUSED
**Cause:** WebSocket server not running  
**Fix:** Run `python websocket_server_integrated.py`

### Issue: Redis timeout error
**Cause:** Redis not running  
**Fix:** Run `"C:\Program Files\Redis\redis-server.exe"`

### Issue: Text never appears in feed
**Cause:** WebSocket connected but no messages  
**Fix:** Check browser console for errors, verify server is sending data

### Issue: Data count doesn't increase
**Cause:** Redis not responding or memory manager error  
**Fix:** Check Redis is running, restart both server and frontend

### Issue: Memory wipe doesn't animate
**Cause:** JavaScript event not firing  
**Fix:** Check Network tab in DevTools, verify "memory_wipe_start" message is received

---

## 📋 Final Checklist (Day-Of-Demo)

### 30 Minutes Before
- [ ] All 4 services started and healthy
- [ ] Test call works end-to-end
- [ ] Ran demo 2-3 times, got timing down
- [ ] Notes printed/on computer
- [ ] Room has power for all terminals
- [ ] Projector/screen working
- [ ] Audio working (for judges to hear system)

### 5 Minutes Before
- [ ] All 4 terminals open and green
- [ ] Browser at http://localhost:3000
- [ ] Console clear of errors (F12)
- [ ] Take a deep breath
- [ ] Smile at judges

### During Demo
- [ ] Speak clearly, explain as you go
- [ ] Point at specific UI elements
- [ ] Count down data points for judges
- [ ] Emphasize "zero persistence"
- [ ] Acknowledge judges' reactions

### After Demo
- [ ] Close call gracefully
- [ ] Answer questions confidently
- [ ] Offer to show code if asked
- [ ] Thank judges

---

## 🎯 Success Criteria

Demo is **SUCCESSFUL** if judges see:

1. ✓ Professional UI with government aesthetic
2. ✓ Real-time text streaming (not instant bulk load)
3. ✓ Data appearing (6 points) then disappearing (→ 0)
4. ✓ Animation showing memory wipe
5. ✓ No errors during demo
6. ✓ System responds naturally (~2-3s per action)

If all 6 criteria met: **You've won.** 🏆

---

## 📞 Emergency Support

**During Demo:**
- **If page won't load:** Refresh (Ctrl+R), restart frontend
- **If WebSocket fails:** Restart WebSocket server, retry
- **If data doesn't appear:** Show backend code, explain architecture
- **If entire system fails:** Pivot to showing code/architecture (judges understand these things happen)

**Recovery Time Budgets:**
- Page refresh: 10 seconds
- Server restart: 30 seconds
- Full system restart: 3-5 minutes (have this planned)

---

## 🏁 You're Ready!

You have:
- ✅ Working Python backend
- ✅ Professional Next.js frontend
- ✅ WebSocket integration
- ✅ Real-time streaming
- ✅ Data sovereignty visualization
- ✅ Complete documentation
- ✅ Demo scripts and guides

**Confidence level: 💯%**

**Time to win Hack4Delhi: NOW**

Go get 'em! 🚀

---

Questions before demo? Check:
1. `FRONTEND_SETUP.md` - Complete setup guide
2. `DEMO_GUIDE.md` - Presentation guide for judges
3. `frontend/README.md` - Component documentation
4. Browser DevTools (F12) - Real-time debugging
5. Terminal output - Look for error messages

**Last thought:** Judges aren't expecting perfection. They're looking for **real innovation**. Your data-sovereignty FSM + zero-persistence memory is genuinely novel. Show it with confidence.

**You've got this!** 🎯✨
