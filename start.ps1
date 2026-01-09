# Sahayta - MCD 311 Sovereign Voice AI
# Unified Start Script
# Launches Backend (FastAPI) and Frontend (Next.js) in persistent terminal windows

Write-Host "==================================" -ForegroundColor Cyan
Write-Host " SAHAYTA - MCD 311 VOICE AI" -ForegroundColor Green
Write-Host " Starting Application..." -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Get the project root directory
$projectRoot = $PSScriptRoot

# Check if Redis is running
Write-Host "Checking Redis..." -ForegroundColor Yellow
$redisProcess = Get-Process redis-server -ErrorAction SilentlyContinue
if (-not $redisProcess) {
    Write-Host "WARNING: Redis not detected. Starting Redis..." -ForegroundColor Red
    try {
        Start-Process "redis-server" -WindowStyle Minimized
        Start-Sleep -Seconds 2
        Write-Host "Redis started successfully." -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Could not start Redis. Install via: choco install redis" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Redis is running." -ForegroundColor Green
}

# Check if Ollama is running
Write-Host "Checking Ollama..." -ForegroundColor Yellow
try {
    $ollamaCheck = Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "Ollama is running." -ForegroundColor Green
} catch {
    Write-Host "WARNING: Ollama not responding. Starting Ollama..." -ForegroundColor Red
    try {
        Start-Process "ollama" "serve" -WindowStyle Minimized
        Start-Sleep -Seconds 3
        Write-Host "Ollama started successfully." -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Could not start Ollama. Install from: https://ollama.ai" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Starting Backend Server..." -ForegroundColor Cyan
# Launch Backend in new PowerShell window
$backendCmd = "cd '$projectRoot'; python -m uvicorn websocket_server_integrated:app --host 0.0.0.0 --port 8000 --reload"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd -WorkingDirectory $projectRoot

Write-Host "Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Starting Frontend Server..." -ForegroundColor Cyan
# Launch Frontend in new PowerShell window
$frontendCmd = "cd '$projectRoot\frontend'; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd -WorkingDirectory "$projectRoot\frontend"

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host " APPLICATION STARTED" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "To stop: Run stop.ps1 or close the terminal windows" -ForegroundColor White
Write-Host "Press any key to exit this launcher..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
