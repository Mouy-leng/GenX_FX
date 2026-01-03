# Automatic Development Environment Setup for Windows
# This script sets up the development environment with Copilot and Stripe tools

Write-Host "🚀 GenX_FX Automatic Development Environment Setup (Windows)" -ForegroundColor Cyan
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-CommandExists {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# Check Node.js and npm
if (Test-CommandExists node) {
    Write-Host "✓ Node.js $(node --version) is installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Node.js is not installed. Please install from https://nodejs.org/" -ForegroundColor Yellow
}

if (Test-CommandExists npm) {
    Write-Host "✓ npm $(npm --version) is installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  npm is not installed" -ForegroundColor Yellow
}

Write-Host ""

# Check Python
if (Test-CommandExists python) {
    Write-Host "✓ Python $(python --version) is installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Python is not installed. Please install from https://python.org/" -ForegroundColor Yellow
}

Write-Host ""

# Install Stripe CLI
Write-Host "📦 Setting up Stripe CLI..." -ForegroundColor Cyan
if (Test-CommandExists stripe) {
    Write-Host "✓ Stripe CLI is already installed ($(stripe --version))" -ForegroundColor Green
} else {
    Write-Host "Installing Stripe CLI..." -ForegroundColor Yellow
    
    if (Test-CommandExists scoop) {
        Write-Host "Using Scoop to install Stripe CLI..." -ForegroundColor Cyan
        scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git
        scoop install stripe
        Write-Host "✓ Stripe CLI installed successfully" -ForegroundColor Green
    } elseif (Test-CommandExists winget) {
        Write-Host "Using winget to install Stripe CLI..." -ForegroundColor Cyan
        winget install stripe.stripe-cli
        Write-Host "✓ Stripe CLI installed successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Neither Scoop nor winget found. Please install Stripe CLI manually:" -ForegroundColor Yellow
        Write-Host "   1. Install Scoop: https://scoop.sh/" -ForegroundColor White
        Write-Host "   2. Then run: scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git" -ForegroundColor White
        Write-Host "   3. Then run: scoop install stripe" -ForegroundColor White
        Write-Host "   Or download from: https://github.com/stripe/stripe-cli/releases/latest" -ForegroundColor White
    }
}

Write-Host ""

# Install Stripe SDK for Node.js
if (Test-Path "ProductionApp/package.json") {
    Write-Host "📦 Installing Stripe SDK for Node.js in ProductionApp..." -ForegroundColor Cyan
    Push-Location ProductionApp
    
    if (Test-CommandExists npm) {
        $packageJson = Get-Content package.json | ConvertFrom-Json
        if ($packageJson.dependencies.stripe) {
            Write-Host "✓ Stripe SDK already in package.json" -ForegroundColor Green
        } else {
            npm install stripe
            Write-Host "✓ Stripe SDK added to ProductionApp" -ForegroundColor Green
        }
    }
    
    Pop-Location
} else {
    Write-Host "ℹ️  ProductionApp not found, skipping Node.js Stripe SDK" -ForegroundColor Gray
}

Write-Host ""

# Install Stripe SDK for Python
Write-Host "📦 Installing Stripe SDK for Python..." -ForegroundColor Cyan
if (Test-CommandExists pip) {
    pip install --user stripe
    Write-Host "✓ Stripe Python SDK installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  pip not found, cannot install Stripe Python SDK" -ForegroundColor Yellow
}

Write-Host ""

# Setup Python environment
if (Test-Path "setup_python_environment.py") {
    Write-Host "🐍 Python environment setup script found" -ForegroundColor Cyan
    Write-Host "   Run manually if needed: python setup_python_environment.py <project_name>" -ForegroundColor White
}

Write-Host ""

# Git hooks setup
Write-Host "🔧 Setting up Git hooks for automatic installation..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path ".git/hooks" | Out-Null

# Create post-merge hook
$postMergeHook = @"
#!/bin/bash
# Post-merge hook - runs after git pull
echo "🔄 Running post-pull setup..."

# Check if there are changes to dependency files
if git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -qE 'package\.json|requirements\.txt|\.devcontainer/'; then
    echo "📦 Dependency files changed, consider running setup:"
    echo "   - For Node.js: cd ProductionApp && npm install"
    echo "   - For Python: pip install -r requirements.txt"
    echo "   - For devcontainer: Rebuild container"
fi
"@

Set-Content -Path ".git/hooks/post-merge" -Value $postMergeHook -NoNewline

# Create post-checkout hook
$postCheckoutHook = @"
#!/bin/bash
# Post-checkout hook - runs after branch checkout
echo "🔄 Checked out branch, remember to:"
echo "   - Update dependencies if needed"
echo "   - Run setup-dev-environment.ps1 if first time"
"@

Set-Content -Path ".git/hooks/post-checkout" -Value $postCheckoutHook -NoNewline

Write-Host "✓ Git hooks installed" -ForegroundColor Green
Write-Host ""

# VSCode extensions recommendation
if ((Test-Path ".vscode") -or (Test-Path "GenX_FX.code-workspace")) {
    Write-Host "📝 VSCode Extensions Recommended:" -ForegroundColor Cyan
    Write-Host "   - GitHub Copilot (GitHub.copilot)" -ForegroundColor White
    Write-Host "   - GitHub Copilot Chat (GitHub.copilot-chat)" -ForegroundColor White
    Write-Host "" 
    Write-Host "   These will be installed automatically if using devcontainer." -ForegroundColor Gray
    Write-Host "   For local VSCode, install them from the Extensions marketplace." -ForegroundColor Gray
}

Write-Host ""
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host "✅ Development environment setup complete!" -ForegroundColor Green
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Stripe: Run 'stripe login' to authenticate" -ForegroundColor White
Write-Host "   2. GitHub Copilot: Sign in when VSCode prompts" -ForegroundColor White
Write-Host "   3. ProductionApp: cd ProductionApp; npm install; npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "📖 Documentation:" -ForegroundColor Cyan
Write-Host "   - GitHub Copilot: https://docs.github.com/en/copilot/using-github-copilot/getting-started-with-github-copilot" -ForegroundColor White
Write-Host "   - Stripe Dev: https://docs.stripe.com/development" -ForegroundColor White
Write-Host ""
