#!/usr/bin/env python3
"""
Auto-launcher: Waits for Ollama models, then runs production demo with REAL LLM
"""

import subprocess
import time
import sys

def get_models():
    """List available Ollama models."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        models = []
        for line in result.stdout.split('\n')[1:]:
            if line.strip():
                parts = line.split()
                if parts:
                    models.append(parts[0])
        return models
    except:
        return []


def wait_for_models():
    """Poll until at least one model is available."""
    print("🕐 Waiting for Ollama models to download...")
    print("   (Checking every 30 seconds)\n")
    
    start = time.time()
    check_count = 0
    
    while True:
        models = get_models()
        check_count += 1
        elapsed = int(time.time() - start)
        
        if models:
            print(f"\n✅ Model ready! ({elapsed}s elapsed, {check_count} checks)")
            for model in models:
                print(f"   • {model}")
            return True
        
        remaining_min = (3600 - elapsed) // 60
        print(f"   Check {check_count:3d} | {elapsed:4d}s elapsed | {remaining_min:2d}min remaining... ", end='', flush=True)
        
        if elapsed > 3600:
            print(f"\n⏱️  1-hour timeout reached. Models not ready.")
            print("   You can still run: python demo_real.py")
            return False
        
        time.sleep(30)


if __name__ == "__main__":
    if wait_for_models():
        print("\n🚀 Launching production demo with real LLM inference...\n")
        time.sleep(2)
        subprocess.run([sys.executable, "demo_real.py"])
    else:
        print("\n⏸️  Models still downloading in background.")
        print("   Run 'python demo_real.py' manually when ready.")
