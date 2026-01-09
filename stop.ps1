# Sahayta - MCD 311 Sovereign Voice AI
# Unified Stop Script
# Terminates all running Backend and Frontend processes

Write-Host "==================================" -ForegroundColor Cyan
Write-Host " SAHAYTA - STOPPING APPLICATION" -ForegroundColor Red
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Stop Backend (Python/Uvicorn)
Write-Host "Stopping Backend Server..." -ForegroundColor Yellow
$backendProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*" -or $_.CommandLine -like "*websocket_server*"
}

if ($backendProcesses) {
    $backendProcesses | ForEach-Object {
        Stop-Process -Id $_.Id -Force
        Write-Host "  Stopped process: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Green
    }
} else {
    Write-Host "  No backend processes found." -ForegroundColor Gray
}

# Stop Frontend (Node/Next.js)
Write-Host "Stopping Frontend Server..." -ForegroundColor Yellow
$frontendProcesses = Get-Process node -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*next*" -or $_.CommandLine -like "*npm*"
}

if ($frontendProcesses) {
    $frontendProcesses | ForEach-Object {
        Stop-Process -Id $_.Id -Force
        Write-Host "  Stopped process: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Green
    }
} else {
    Write-Host "  No frontend processes found." -ForegroundColor Gray
}

# Optional: Stop Redis (if you want to fully shut down)
# Uncomment the following lines if you want to stop Redis as well
# Write-Host "Stopping Redis..." -ForegroundColor Yellow
# $redisProcesses = Get-Process redis-server -ErrorAction SilentlyContinue
# if ($redisProcesses) {
#     $redisProcesses | Stop-Process -Force
#     Write-Host "  Redis stopped." -ForegroundColor Green
# }

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host " APPLICATION STOPPED" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
