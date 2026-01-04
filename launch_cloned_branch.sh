#!/bin/bash

# GenX_FX Repository Launch Script for Cloned Branch
# Organization: A6-9V
# Purpose: Quick launch script for the copilot/launch-repository-clone branch

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              🚀 GenX_FX Repository Launcher                 ║"
echo "║           Launch on Cloned Branch (Unix/Linux/Mac)          ║"
echo "║                    Organization: A6-9V                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Verify git repository
echo -e "${BLUE}[INFO]${NC} Step 1: Verifying Git repository..."
if [ ! -d ".git" ]; then
    echo -e "${RED}[ERROR]${NC} Not a Git repository. Please run this script from the GenX_FX root directory."
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Git repository detected"
echo ""

# Step 2: Check current branch
echo -e "${BLUE}[INFO]${NC} Step 2: Checking current branch..."
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${YELLOW}Current branch:${NC} $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" != "copilot/launch-repository-clone" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Not on the expected branch."
    read -p "Do you want to checkout copilot/launch-repository-clone? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git checkout copilot/launch-repository-clone
        echo -e "${GREEN}[OK]${NC} Switched to copilot/launch-repository-clone branch"
    fi
else
    echo -e "${GREEN}[OK]${NC} Already on copilot/launch-repository-clone branch"
fi
echo ""

# Step 3: Verify repository structure
echo -e "${BLUE}[INFO]${NC} Step 3: Verifying repository structure..."
REQUIRED_FILES=(
    "A6-9V_Master_System_README.md"
    "README-local.md"
    "A6-9V_Enhanced_Master_Launcher.bat"
    "REPOSITORY_LAUNCH_GUIDE.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}[✓]${NC} Found: $file"
    else
        echo -e "${RED}[✗]${NC} Missing: $file"
    fi
done
echo ""

# Step 4: Check Python environment
echo -e "${BLUE}[INFO]${NC} Step 4: Checking Python environment..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}[OK]${NC} Python detected: $PYTHON_VERSION"
else
    echo -e "${YELLOW}[WARNING]${NC} Python3 not found in PATH"
fi
echo ""

# Step 5: Check virtual environment
echo -e "${BLUE}[INFO]${NC} Step 5: Checking virtual environment..."
if [ -d "A6-9V/Trading/GenX_FX/venv" ]; then
    echo -e "${GREEN}[OK]${NC} Virtual environment found at A6-9V/Trading/GenX_FX/venv"
else
    echo -e "${YELLOW}[WARNING]${NC} Virtual environment not found"
    echo -e "${BLUE}[INFO]${NC} You may need to create it manually"
fi
echo ""

# Step 6: Display configuration summary
echo -e "${BLUE}[INFO]${NC} Step 6: Configuration Summary"
echo "════════════════════════════════════════════════════════════════"
echo -e "${YELLOW}Repository:${NC} Mouy-leng/GenX_FX"
echo -e "${YELLOW}Branch:${NC} $CURRENT_BRANCH"
echo -e "${YELLOW}Working Directory:${NC} $(pwd)"
echo -e "${YELLOW}Git Status:${NC}"
git status --short
echo ""

# Step 7: Display next steps
echo -e "${GREEN}[SUCCESS]${NC} Repository verification complete!"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo -e "${BLUE}Next Steps:${NC}"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "📖 For detailed instructions, read:"
echo "   • REPOSITORY_LAUNCH_GUIDE.md - Complete launch guide"
echo "   • A6-9V_Master_System_README.md - System overview"
echo "   • README-local.md - Local workspace information"
echo ""
echo "🖥️  On Windows, launch the system with:"
echo "   • A6-9V_Enhanced_Master_Launcher.bat"
echo ""
echo "🐍 For Python components:"
echo "   cd A6-9V/Trading/GenX_FX"
echo "   source venv/bin/activate  # On Unix/Linux/Mac"
echo "   python main.py"
echo ""
echo "🤖 MT5 Trading Platform Setup:"
echo "   • Account: Exness-MT5Trial8 (Demo)"
echo "   • Balance: 39,499.31 USD"
echo "   • Server: Exness-MT5Trail8"
echo ""
echo "📊 Expert Advisors Available:"
echo "   • ExpertMAPSAR_Enhanced"
echo "   • ExpertMACD"
echo "   • ExpertMAMA"
echo "   • ExpertMAPSAR"
echo "   • ExpertMAPSARSizeOptimized"
echo "   • bridges3rd"
echo ""
echo "🔗 Additional Resources:"
echo "   • Code With Me: https://code-with-me.global.jetbrains.com/ZhaX8frcoZS0qveUMv8vAg"
echo "   • Documentation: docs/README.md"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo -e "${GREEN}🎯 A6-9V GenX_FX Repository Ready for Launch!${NC}"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Optional: Open documentation
read -p "Would you like to view the launch guide now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v less &> /dev/null; then
        less REPOSITORY_LAUNCH_GUIDE.md
    elif command -v more &> /dev/null; then
        more REPOSITORY_LAUNCH_GUIDE.md
    else
        cat REPOSITORY_LAUNCH_GUIDE.md
    fi
fi

exit 0
