# Setup Jules Communication Environment Variables
# GenX_FX Trading Platform - Multi-Agent Communication

Write-Host "Setting up Jules Communication Environment..." -ForegroundColor Green

# Read environment file
$envFile = "jules_communication.env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^([^#][^=]+)=(.*)$") {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            
            # Set environment variable for current session
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
            
            # Set environment variable permanently for user
            [Environment]::SetEnvironmentVariable($name, $value, "User")
            
            Write-Host "Set $name = $value" -ForegroundColor Yellow
        }
    }
    
    Write-Host "`nJules Communication Environment Setup Complete!" -ForegroundColor Green
    Write-Host "`nKey Settings:" -ForegroundColor Cyan
    Write-Host "- Jules HTTP Port: $env:JULES_HTTP_PORT" -ForegroundColor White
    Write-Host "- API URL: $env:JULES_API_URL" -ForegroundColor White
    Write-Host "- Gateway Port: $env:MULTI_AGENT_GATEWAY_PORT" -ForegroundColor White
    Write-Host "- Health Check: $env:HEALTH_CHECK_URL" -ForegroundColor White
    
    Write-Host "`nEnvironment variables have been set for the current session and saved permanently." -ForegroundColor Green
} else {
    Write-Host "Error: jules_communication.env file not found!" -ForegroundColor Red
}

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")