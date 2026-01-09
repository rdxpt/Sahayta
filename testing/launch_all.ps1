# Launch Script for McDonald 311 Sovereign AI
# Starts Redis (if needed), Backend, and Frontend in separate windows

Write-Host "Starting System..."

# 1. Start Redis check
$redisPort = 6379
$redisOpen = (Get-NetTCPConnection -LocalPort $redisPort -ErrorAction SilentlyContinue)
if (-not $redisOpen) {
    Write-Host "Starting Redis..."
    Start-Process -FilePath "C:\Program Files\Redis\redis-server.exe" -WindowStyle Minimized
    Start-Sleep -Seconds 2
} else {
    Write-Host "Redis already running."
}

# 2. Start Backend
Write-Host "Starting Backend (Port 8000)..."
$env:PYTHONIOENCODING="utf-8"
Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "websocket_server_integrated.py" -WindowStyle Minimized

# 3. Start Frontend
Write-Host "Starting Frontend..."
# Use direct launch script to avoid npm issues
Start-Process -FilePath "powershell.exe" -ArgumentList "-ExecutionPolicy Bypass -File .\launch_frontend_direct.ps1" -WindowStyle Normal

Write-Host "System Launch Initiated."
Write-Host "Backend: http://localhost:8000/health"
Write-Host "Frontend: http://localhost:3000 (or 3001)"
