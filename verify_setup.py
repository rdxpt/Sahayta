#!/usr/bin/env python3
"""
Verification Script - Checks all components are working
Run this before the Hack4Delhi demo to ensure everything is ready!
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_redis():
    """Check Redis connectivity."""
    print("\n[CHECK 1] Redis Connection")
    print("-" * 50)
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("✓ Redis is running and accessible")
        info = r.info('memory')
        print(f"  Memory used: {info['used_memory'] / 1024 / 1024:.2f} MB")
        return True
    except Exception as e:
        print(f"✗ Redis check failed: {e}")
        print("  Start Redis with: redis-server")
        return False

def check_ollama():
    """Check Ollama connectivity."""
    print("\n[CHECK 2] Ollama Connection")
    print("-" * 50)
    try:
        import ollama
        client = ollama.Client(host='http://localhost:11434')
        models = client.list()
        print(f"✓ Ollama is running and accessible")
        print(f"  Available models:")
        for model in models['models']:
            print(f"    - {model['name']}")
        
        # Check for required models
        model_names = [m['name'] for m in models['models']]
        has_mistral = any('mistral' in m for m in model_names)
        has_neural = any('neural' in m for m in model_names)
        
        if not has_mistral:
            print("  ⚠ Missing 'mistral' model. Run: ollama pull mistral")
        if not has_neural:
            print("  ⚠ Missing 'neural-chat' model. Run: ollama pull neural-chat")
        
        return has_mistral and has_neural
    except Exception as e:
        print(f"✗ Ollama check failed: {e}")
        print("  Start Ollama with: ollama serve")
        print("  Then pull models:")
        print("    ollama pull mistral")
        print("    ollama pull neural-chat")
        return False

def check_imports():
    """Check all Python imports."""
    print("\n[CHECK 3] Python Imports")
    print("-" * 50)
    
    required_modules = [
        'redis',
        'langgraph',
        'langchain',
        'pydantic',
        'ollama',
        'pyttsx3',
        'numpy'
    ]
    
    all_ok = True
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - Run: pip install {module}")
            all_ok = False
    
    return all_ok

def check_config():
    """Check configuration."""
    print("\n[CHECK 4] Configuration Files")
    print("-" * 50)
    
    files = [
        'config/settings.py',
        'src/agent_state.py',
        'src/memory_manager.py',
        'src/llm_integration.py',
        'src/workflow.py',
        '.env',
        'main_demo.py'
    ]
    
    all_ok = True
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✓ {file} ({size} bytes)")
        else:
            print(f"✗ {file} - File not found")
            all_ok = False
    
    return all_ok

def check_memory_manager():
    """Test MemoryManager functionality."""
    print("\n[CHECK 5] Memory Manager (Redis Operations)")
    print("-" * 50)
    
    try:
        from src.memory_manager import memory_manager
        from src.agent_state import AgentState
        from datetime import datetime
        import uuid
        
        # Create test session
        test_id = f"test_{uuid.uuid4().hex[:6]}"
        state = AgentState(
            session_id=test_id,
            call_timestamp=datetime.now().isoformat(),
            citizen_name="Test Citizen",
            citizen_phone="+91-9999999999"
        )
        
        # Store
        memory_manager.store_session(state)
        print(f"✓ Stored session {test_id}")
        
        # Retrieve
        retrieved = memory_manager.retrieve_session(test_id)
        if retrieved:
            print(f"✓ Retrieved session (name: {retrieved.citizen_name})")
        else:
            print(f"✗ Could not retrieve session")
            return False
        
        # Wipe
        result = memory_manager.memory_wipe_node(retrieved)
        if result.get('status') == 'WIPED_AND_CLOSED':
            print(f"✓ Memory wipe successful")
        else:
            print(f"✗ Memory wipe failed: {result.get('status')}")
            return False
        
        # Verify wipe
        verify = memory_manager.retrieve_session(test_id)
        if verify is None:
            print(f"✓ Verified: Data deleted from Redis")
        else:
            print(f"✗ Data still exists after wipe")
            return False
        
        return True
    
    except Exception as e:
        print(f"✗ Memory manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all checks."""
    print("\n" + "=" * 70)
    print("  MCD 311 SOVEREIGN VOICE AI - SYSTEM VERIFICATION")
    print("=" * 70)
    
    results = {
        "Redis": check_redis(),
        "Ollama": check_ollama(),
        "Imports": check_imports(),
        "Config Files": check_config(),
        "Memory Manager": check_memory_manager(),
    }
    
    print("\n" + "=" * 70)
    print("  VERIFICATION SUMMARY")
    print("=" * 70)
    
    for check, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status:8} {check}")
    
    all_passed = all(results.values())
    
    print("=" * 70)
    
    if all_passed:
        print("\n✓ ALL CHECKS PASSED! Ready to run main_demo.py")
        print("\nNext step:")
        print("  python main_demo.py")
        return 0
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Start Redis: redis-server")
        print("  2. Start Ollama: ollama serve")
        print("  3. Pull models: ollama pull mistral neural-chat")
        print("  4. Activate venv: .\\venv\\Scripts\\activate")
        return 1

if __name__ == "__main__":
    sys.exit(main())
