# GenX FX Trading Platform Startup Script for Local Windows Machine
# This script starts and monitors all required services for 24/7 operation

# Enable error handling
$ErrorActionPreference = "Stop"

# Function to write logs with timestamp
function Write-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message"
    Add-Content -Path ".\logs\startup.log" -Value "[$timestamp] $Message"
}

# Function to check if a Docker container is healthy
function Test-ContainerHealth {
    param($ContainerName)
    $status = docker inspect --format='{{.State.Health.Status}}' $ContainerName 2>$null
    return $status -eq "healthy"
}

# Create necessary directories
$dirs = @("logs", "data", "expert-advisors", "reports")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir
        Write-Log "Created directory: $dir"
    }
}

# Check if Docker is running
Write-Log "Checking Docker service..."
$dockerService = Get-Service -Name "Docker" -ErrorAction SilentlyContinue
if ($null -eq $dockerService) {
    Write-Log "Error: Docker service not found. Please install Docker Desktop"
    exit 1
}
if ($dockerService.Status -ne "Running") {
    Write-Log "Starting Docker service..."
    Start-Service -Name "Docker"
    Start-Sleep -Seconds 10
}

# Start containers using docker-compose
try {
    Write-Log "Starting containers with docker-compose..."
    docker-compose -f docker-compose.local.yml up -d
    Start-Sleep -Seconds 30
} catch {
    Write-Log "Error starting containers: $_"
    exit 1
}

# Verify container health
$containers = @("genxdb_fx_mysql", "genx-redis", "genx-backend", "genxdb_fx_trading")
foreach ($container in $containers) {
    Write-Log "Checking health of container: $container"
    if (-not (Test-ContainerHealth $container)) {
        Write-Log "Warning: Container $container may not be healthy"
    }
}

# Start Python trading bot if not running in container
if (Test-Path ".\main.py") {
    Write-Log "Starting Python trading bot..."
    $env:PYTHONPATH = "."
    Start-Process -FilePath "python" -ArgumentList "main.py" -NoNewWindow
}

# Install health monitor requirements
Write-Log "Installing health monitor requirements..."
pip install -r health_monitor_requirements.txt

# Start health monitor in background
Write-Log "Starting health monitor..."
Start-Process -FilePath "python" -ArgumentList "health_monitor.py" -NoNewWindow

# Monitor loop
Write-Log "Starting monitoring loop..."
while ($true) {
    try {
        # Check container status
        $containers | ForEach-Object {
            $status = docker ps -f name=$_ --format "{{.Status}}"
            if ($status -notmatch "Up") {
                Write-Log "Container $_ is down, attempting restart..."
                docker start $_
            }
        }

        # Check API health
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8080/health" -Method Get
            if ($response.StatusCode -ne 200) {
                Write-Log "Warning: API health check failed"
            }
        } catch {
            Write-Log "Error checking API health: $_"
        }

        # Check trading bot process if running locally
        $tradingBot = Get-Process -Name "python" -ErrorAction SilentlyContinue | 
                     Where-Object { $_.CommandLine -match "main.py" }
        if ($null -eq $tradingBot) {
            Write-Log "Trading bot process not found, restarting..."
            Start-Process -FilePath "python" -ArgumentList "main.py" -NoNewWindow
        }

        # Log system status
        Write-Log "System running - All services operational"
        
        # Wait before next check
        Start-Sleep -Seconds 60
        
    } catch {
        Write-Log "Error in monitoring loop: $_"
        Start-Sleep -Seconds 30
    }
}