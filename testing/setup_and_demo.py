#!/usr/bin/env python3
"""
MCD 311 Automated Setup & Demo Launcher
Waits for model downloads, then runs production demo
"""

import subprocess
import time
import sys

def wait_for_model(model_name, timeout=3600):
    """Wait for a model to be available."""
    print(f"\n⏳ Waiting for {model_name} to be available...")
    print(f"   (This may take 5-30 minutes depending on your internet)")
    
    start_time = time.time()
    last_size = 0
    
    while time.time() - start_time < timeout:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if model_name in result.stdout:
            print(f"\n✓ {model_name} is ready!")
            return True
        
        # Show progress
        for line in result.stdout.split('\n'):
            if 'manifest' in line.lower() or 'pulling' in line.lower():
                print(f"   {line}")
        
        time.sleep(30)  # Check every 30 seconds
    
    return False


def main():
    print("=" * 80)
    print("  MCD 311 SOVEREIGN VOICE AI - AUTOMATED SETUP")
    print("=" * 80)
    
    # List currently downloading/available models
    print("\n📦 Checking model status...")
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    current_models = []
    for line in result.stdout.split('\n')[1:]:
        if line.strip():
            parts = line.split()
            if parts:
                current_models.append(parts[0])
    
    print(f"   Available models: {current_models if current_models else 'None yet'}")
    
    # Wait for at least one model
    if not current_models:
        print("\n📥 Downloading Mistral for Fast Path (4.4GB)...")
        print("   Download may take 10-30 minutes. Please wait...")
        
        if not wait_for_model("mistral"):
            print("\n✗ Mistral download timed out or failed")
            print("   Try manually: ollama pull mistral")
            return False
    
    print("\n✅ Setup complete! Models ready.")
    print("\n🚀 Launching production demo...\n")
    
    # Run the production demo
    result = subprocess.run(
        [sys.executable, "demo_production.py"],
        cwd="."
    )
    
    return result.returncode == 0


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✗ Setup interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
