#!/bin/bash
# Automatic Development Environment Setup
# This script runs automatically to install required tools and dependencies

set -e

echo "🚀 GenX_FX Automatic Development Environment Setup"
echo "=================================================="
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    MSYS*)      MACHINE=Msys;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "🖥️  Detected OS: ${MACHINE}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Node.js and npm
if command_exists node; then
    echo "✓ Node.js $(node --version) is installed"
else
    echo "⚠️  Node.js is not installed. Please install Node.js from https://nodejs.org/"
    echo "   Recommended: Use nvm (Node Version Manager)"
fi

if command_exists npm; then
    echo "✓ npm $(npm --version) is installed"
else
    echo "⚠️  npm is not installed"
fi

echo ""

# Check Python
if command_exists python3; then
    echo "✓ Python $(python3 --version) is installed"
elif command_exists python; then
    echo "✓ Python $(python --version) is installed"
else
    echo "⚠️  Python is not installed. Please install Python from https://python.org/"
fi

echo ""

# Install Stripe CLI
echo "📦 Setting up Stripe CLI..."
if command_exists stripe; then
    echo "✓ Stripe CLI is already installed ($(stripe --version))"
else
    echo "Installing Stripe CLI..."
    
    case "${MACHINE}" in
        Linux)
            if command_exists curl && command_exists sudo; then
                curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg >/dev/null
                echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee -a /etc/apt/sources.list.d/stripe.list
                sudo apt update && sudo apt install -y stripe
                echo "✓ Stripe CLI installed successfully"
            else
                echo "⚠️  Cannot install Stripe CLI automatically. Please install manually:"
                echo "   Visit: https://stripe.com/docs/stripe-cli#install"
            fi
            ;;
        Mac)
            if command_exists brew; then
                brew install stripe/stripe-cli/stripe
                echo "✓ Stripe CLI installed successfully"
            else
                echo "⚠️  Homebrew not found. Please install Homebrew first:"
                echo "   Visit: https://brew.sh/"
                echo "   Then run: brew install stripe/stripe-cli/stripe"
                echo "   Or visit: https://stripe.com/docs/stripe-cli#install"
            fi
            ;;
        MinGw|Msys|Cygwin)
            echo "⚠️  For Windows, please install Stripe CLI using:"
            echo "   scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git"
            echo "   scoop install stripe"
            echo "   Or download from: https://github.com/stripe/stripe-cli/releases/latest"
            ;;
        *)
            echo "⚠️  Unknown OS. Please install Stripe CLI manually:"
            echo "   Visit: https://stripe.com/docs/stripe-cli#install"
            ;;
    esac
fi

echo ""

# Install Stripe SDK for Node.js (in ProductionApp if it exists)
if [ -d "ProductionApp" ] && [ -f "ProductionApp/package.json" ]; then
    echo "📦 Installing Stripe SDK for Node.js in ProductionApp..."
    cd ProductionApp
    if command_exists npm; then
        if grep -q '"stripe"' package.json; then
            echo "✓ Stripe SDK already in package.json"
        else
            npm install stripe || echo "⚠️  Failed to install Stripe SDK in ProductionApp"
            echo "✓ Stripe SDK added to ProductionApp"
        fi
    fi
    cd ..
else
    echo "ℹ️  ProductionApp not found, skipping Node.js Stripe SDK"
fi

echo ""

# Install Stripe SDK for Python
echo "📦 Installing Stripe SDK for Python..."
if command_exists pip3; then
    pip3 install --user stripe
    echo "✓ Stripe Python SDK installed"
elif command_exists pip; then
    pip install --user stripe
    echo "✓ Stripe Python SDK installed"
else
    echo "⚠️  pip not found, cannot install Stripe Python SDK"
fi

echo ""

# Setup Python environment (if setup script exists)
if [ -f "setup_python_environment.py" ]; then
    echo "🐍 Python environment setup script found"
    echo "   Run manually if needed: python3 setup_python_environment.py <project_name>"
fi

echo ""

# Git hooks setup
echo "🔧 Setting up Git hooks for automatic installation..."
mkdir -p .git/hooks

# Create post-merge hook (runs after git pull)
cat > .git/hooks/post-merge << 'HOOK_EOF'
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
HOOK_EOF

chmod +x .git/hooks/post-merge

# Create post-checkout hook (runs after git checkout)
cat > .git/hooks/post-checkout << 'HOOK_EOF'
#!/bin/bash
# Post-checkout hook - runs after branch checkout
echo "🔄 Checked out branch, remember to:"
echo "   - Update dependencies if needed"
echo "   - Run setup-dev-environment.sh if first time"
HOOK_EOF

chmod +x .git/hooks/post-checkout

echo "✓ Git hooks installed"
echo ""

# VSCode extensions recommendation
if [ -d ".vscode" ] || [ -f "GenX_FX.code-workspace" ]; then
    echo "📝 VSCode Extensions Recommended:"
    echo "   - GitHub Copilot (GitHub.copilot)"
    echo "   - GitHub Copilot Chat (GitHub.copilot-chat)"
    echo ""
    echo "   These will be installed automatically if using devcontainer."
    echo "   For local VSCode, install them from the Extensions marketplace."
fi

echo ""
echo "=================================================="
echo "✅ Development environment setup complete!"
echo "=================================================="
echo ""
echo "📚 Next Steps:"
echo "   1. Stripe: Run 'stripe login' to authenticate"
echo "   2. GitHub Copilot: Sign in when VSCode prompts"
echo "   3. ProductionApp: cd ProductionApp && npm install && npm run dev"
echo ""
echo "📖 Documentation:"
echo "   - GitHub Copilot: https://docs.github.com/en/copilot/using-github-copilot/getting-started-with-github-copilot"
echo "   - Stripe Dev: https://docs.stripe.com/development"
echo ""
