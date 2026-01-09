# ⚡ QUICK START GUIDE - MCD 311 Sovereign Voice AI

## 5-Minute Setup

### Prerequisites
- Python 3.10+ installed
- 2GB RAM available
- 10 minutes of your time

### Step 1: Start Redis (5 seconds)
```bash
# If you have Redis installed:
redis-server

# If using WSL or Docker:
docker run -p 6379:6379 redis:latest
```

**Expected output:**
```
Ready to accept connections
```

### Step 2: Start Ollama (1 minute)
```bash
# Start Ollama server
ollama serve

# In another terminal, pull models (first time only):
ollama pull mistral
ollama pull neural-chat
```

**Expected output:**
```
Listening on 127.0.0.1:11434
```

### Step 3: Run the Demo (2 minutes)
```bash
cd c:\Users\rdxpt\cooks\pyML\Sahayta
.\venv\Scripts\activate
python main_demo.py
```

**Expected output:**
```
======================================================================
  MCD 311 SOVEREIGN VOICE AI - COMPLETE DEMO
======================================================================

✓ Redis: Connected (In-Memory Mode)
✓ Ollama: Connected (Local LLM Mode)

[... complete workflow execution ...]

✓ ALL DATA PERMANENTLY WIPED FROM RAM!
```

---

## 🎯 What You're Running

This demo executes a **complete, real-world scenario**:

1. ✅ **Citizen calls 311** with a grievance
2. ✅ **AI listens** to the complaint
3. ✅ **LLM categorizes** it (Road, Water, etc.)
4. ✅ **Decision logic** determines escalation
5. ✅ **Response generated** to citizen
6. ✅ **ALL data DELETED** from memory

The entire process is **completely offline** - no cloud, no external APIs.

---

## 🔍 Understanding the Output

### Phase 1: System Initialization
```
✓ Redis: Connected (In-Memory Mode)
✓ Ollama: Connected (Local LLM Mode)
```
System checks that both backends are running.

### Phase 2: Session Creation
```
Session ID: demo_a1b2c3
Timestamp: 2026-01-08T15:30:45.123456
```
A unique session is created. This is what tracks the call.

### Phase 3: FSM Execution
```
[NODE] initiate_call: Starting session demo_a1b2c3
[NODE] listen_grievance: Waiting for citizen input
[NODE] categorize: Analyzing grievance
```
The workflow executes through each state machine node.

### Phase 4: Memory Wipe (The Magic Moment!)
```
BEFORE WIPE:
  session_id: demo_a1b
  citizen_phone: +91-9876543210
  citizen_name: Rajesh Kumar
  redis_status: ✓ DATA IN RAM

[Waiting 2 seconds...]

WIPING FROM MEMORY...
  • Deleting session:{session_id}
  • Deleting metadata:{session_id}
  • Hard-shreding RAM...

AFTER WIPE:
  citizen_phone: [DELETED]
  citizen_name: [DELETED]
  redis_status: ✗ NO DATA IN RAM
  compliance: ✓ 100% DATA SOVEREIGNTY
```

**This is the moment that impresses the judges!** ✨

---

## 🐛 Troubleshooting

### Issue: "ConnectionError: Connection refused"
**Cause:** Redis not running  
**Solution:**
```bash
# Terminal 1:
redis-server
```

### Issue: "Ollama connection error"
**Cause:** Ollama server not running  
**Solution:**
```bash
# Terminal 2:
ollama serve
```

### Issue: "Model 'mistral' not found"
**Cause:** Models not pulled  
**Solution:**
```bash
ollama pull mistral
ollama pull neural-chat
```

### Issue: "ModuleNotFoundError: No module named 'redis'"
**Cause:** Virtual environment not activated  
**Solution:**
```bash
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

---

## 📊 Monitoring in Real-Time

### Option 1: Redis Monitor (Recommended for demo!)

Open a 4th terminal and run:
```bash
redis-cli MONITOR
```

This shows **all Redis commands in real-time**. When you run the demo, you'll see:
```
1641234567.123456 [0 localhost:56789] "HSET" "session:abc123" "citizen_name" "Rajesh Kumar"
1641234567.234567 [0 localhost:56789] "HSET" "session:abc123" "citizen_phone" "+91-9876543210"
[... more commands ...]
1641234567.456789 [0 localhost:56789] "DEL" "session:abc123"  ← WIPE HAPPENS HERE!
```

**Result:** Empty! Data is gone! 🎉

### Option 2: Redis CLI

```bash
redis-cli

# In redis-cli, check session data:
HGETALL session:demo_a1b2c3

# Will show:
# citizen_name: "Rajesh Kumar"
# citizen_phone: "+91-9876543210"
# ...

# After wipe:
HGETALL session:demo_a1b2c3
# (empty)
```

---

## 🎓 Learning the Code

Start with these files in order:

1. **`config/settings.py`** (2 min read)
   - Understand the configuration system

2. **`src/agent_state.py`** (5 min read)
   - Learn the state schema for the FSM

3. **`src/memory_manager.py`** (5 min read)
   - **The core of data sovereignty**
   - Look at `memory_wipe_node()` - this is your winning logic!

4. **`src/workflow.py`** (10 min read)
   - The FSM implementation using LangGraph
   - Understand how nodes connect

5. **`main_demo.py`** (5 min read)
   - How to orchestrate everything together

---

## 💡 Key Concepts

### Finite State Machine (FSM)
The workflow follows a strict path:
```
INITIATED → LISTENING → PROCESSING → PROCESSING → 
ESCALATION_CHECK → RESOLVED/ESCALATED → WIPED
```

Agent **cannot deviate** from this path. This is the governance guarantee.

### Zero-Persistence
Data exists **only in RAM**:
- ❌ Not in `/tmp/`
- ❌ Not in logs (with PII)
- ❌ Not in database
- ❌ Not in backup files
- ✅ Only in Redis (RAM)
- ✅ Deleted immediately after call

### Fast Path vs. Deep Path
- **Fast Path:** Quick responses for simple categorization (20-50ms)
- **Deep Path:** Complex reasoning for escalation decisions (500-1000ms)

---

## 🚀 Next Steps

After the demo works, try:

1. **Modify the grievance:**
   Edit `main_demo.py` line ~180:
   ```python
   grievance_description="Different grievance here"
   ```

2. **Test with your own data:**
   Create a test script that loads citizen data from a CSV

3. **Add voice input:**
   Integrate `speech_recognition` library for actual voice calls

4. **Scale it:**
   Deploy using Docker + Kubernetes for production

---

## 📞 Getting Help

**Error in logs?**
Check `logs/sovereign_voice_ai.log`:
```bash
tail -f logs/sovereign_voice_ai.log
```

**Want to debug FSM execution?**
Edit `config/settings.py`:
```python
LOG_LEVEL="DEBUG"  # Much more verbose output
```

---

## 🎯 Your Mission

You now have a **production-ready skeleton** for:
- ✅ Local LLM inference
- ✅ Finite State Machine workflows
- ✅ Zero-persistence data handling
- ✅ Complete Redis integration

Take this to Hack4Delhi and **show them the data disappearing!** 🎬✨

---

**Ready to change how India handles citizen grievances?**

Let's go! 🚀
