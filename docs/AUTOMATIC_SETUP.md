# Automatic Development Environment Setup

This document explains how the GenX_FX repository automatically sets up development tools when you pull or clone the repository.

## 🚀 What Gets Installed Automatically

### GitHub Copilot
- **GitHub Copilot** extension for AI-powered code completion
- **GitHub Copilot Chat** for conversational AI assistance
- Automatically configured in VSCode devcontainer
- [Documentation](https://docs.github.com/en/copilot/using-github-copilot/getting-started-with-github-copilot)

### Stripe Development Tools
- **Stripe CLI** for local Stripe API testing
- **Stripe SDK for Node.js** (in ProductionApp)
- **Stripe SDK for Python** for Python projects
- [Documentation](https://docs.stripe.com/development)

### Additional Tools
- Node.js and npm dependencies
- Python packages and virtual environments
- Git hooks for automatic setup triggers

## 🔧 Setup Methods

### Method 1: Using DevContainer (Recommended)

If you're using VSCode with the Dev Containers extension:

1. Clone the repository
2. Open in VSCode
3. Click "Reopen in Container" when prompted
4. Everything installs automatically! ✨

The devcontainer will:
- Install all required extensions (including Copilot)
- Set up development environment
- Install Stripe CLI and SDKs
- Configure all tools

### Method 2: Manual Setup (Local Development)

#### Linux/macOS
```bash
# Clone the repository
git clone <repository-url>
cd GenX_FX

# Run the setup script
./setup-dev-environment.sh
```

#### Windows
```powershell
# Clone the repository
git clone <repository-url>
cd GenX_FX

# Run the setup script
.\setup-dev-environment.ps1
```

### Method 3: Automatic on Pull

Git hooks are installed that will:
- Detect changes to dependency files after `git pull`
- Remind you to update dependencies
- Suggest running setup scripts when needed

## 📦 What Happens on Each Pull

When you run `git pull`, the repository checks for:
- Changes to `package.json` → Suggests running `npm install`
- Changes to `requirements.txt` → Suggests running `pip install`
- Changes to `.devcontainer/` → Suggests rebuilding container

## 🔑 First-Time Setup Steps

### 1. GitHub Copilot
After the extensions are installed:
1. VSCode will prompt you to sign in to GitHub
2. Follow the authentication flow
3. Start coding with AI assistance!

**Note:** GitHub Copilot requires a subscription or is free for verified students/open source maintainers.

### 2. Stripe CLI
After installation:
```bash
# Authenticate with Stripe
stripe login

# Test the connection
stripe listen
```

You'll need a Stripe account. Sign up at [stripe.com](https://stripe.com).

## 📋 Prerequisites

Before running the setup scripts, ensure you have:

- **Git** - Version control
- **Node.js & npm** - JavaScript runtime (v16+ recommended)
- **Python** - Python 3.8+ recommended
- **VSCode** - For Copilot integration (optional but recommended)

### Installing Prerequisites

#### Windows
- Use [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) or [Scoop](https://scoop.sh/)
- Or download from official websites

#### macOS
- Use [Homebrew](https://brew.sh/)
```bash
brew install node python git
```

#### Linux
- Use your package manager (apt, yum, dnf)
```bash
# Debian/Ubuntu
sudo apt install nodejs npm python3 python3-pip git

# Fedora/RHEL
sudo dnf install nodejs python3 python3-pip git
```

## 🛠️ Manual Installation

If automatic installation doesn't work:

### Stripe CLI

**Windows (Scoop):**
```powershell
scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git
scoop install stripe
```

**macOS (Homebrew):**
```bash
brew install stripe/stripe-cli/stripe
```

**Linux:**
```bash
curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg
echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee /etc/apt/sources.list.d/stripe.list
sudo apt update && sudo apt install stripe
```

### GitHub Copilot

Install from VSCode Extensions marketplace:
1. Open VSCode
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "GitHub Copilot"
4. Install both "GitHub Copilot" and "GitHub Copilot Chat"

## 🔍 Troubleshooting

### Copilot Not Working
- Ensure you're signed in to GitHub in VSCode
- Check your Copilot subscription status
- Restart VSCode after installation

### Stripe CLI Not Found
- Add Stripe to your PATH
- Verify installation: `stripe --version`
- Try manual installation (see above)

### Dependencies Not Installing
- Check internet connection
- Verify npm/pip are in PATH
- Run setup scripts with elevated permissions if needed

### Git Hooks Not Running
- Ensure hooks have execute permissions: `chmod +x .git/hooks/*`
- Check `.git/hooks/` directory exists
- Re-run setup script to recreate hooks

## 📚 Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Stripe API Documentation](https://docs.stripe.com/api)
- [Stripe CLI Documentation](https://docs.stripe.com/stripe-cli)
- [VSCode Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

## 🤝 Contributing

When adding new dependencies or tools:
1. Update the setup scripts (`setup-dev-environment.sh` and `.ps1`)
2. Update `.devcontainer/post-create.sh`
3. Update this README
4. Test on multiple platforms if possible

## 📝 License

See main repository LICENSE file.
