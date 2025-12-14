# 🚀 A6-9V Auto-Startup Quick Start

## One-Time Setup (5 Minutes)

### Step 1: Install Auto-Startup
1. Navigate to: `C:\Users\lengk\Dropbox\OneDrive\Desktop\`
2. Double-click: `Install_AutoStartup.bat`
3. Select option: **1** (Install Auto-Startup)
4. Wait for confirmation: ✅ Success message

### Step 2: Test the Setup
1. Double-click: `A6-9V_Silent_Launcher.vbs` to test
2. Verify all systems start correctly
3. Close all windows

### Step 3: Restart & Verify
1. Restart your computer
2. Log in normally
3. Wait ~2 minutes for full system startup
4. Verify all components are running

---

## Daily Use

### Normal Operation
- **Just log in** - System starts automatically
- **Wait ~2 minutes** - All components initialize
- **Desktop auto-locks** - After 15 seconds (security)

### Quick Commands

| Action | Command |
|--------|---------|
| **Check if enabled** | Run `Install_AutoStartup.bat` → Option 3 |
| **Disable auto-start** | Run `Install_AutoStartup.bat` → Option 2 |
| **Re-enable auto-start** | Run `Install_AutoStartup.bat` → Option 1 |
| **Skip startup once** | Hold `Shift` during Windows login |
| **Test manually** | Double-click `A6-9V_Silent_Launcher.vbs` |

---

## What Starts Automatically?

✅ **MetaTrader Platforms**
- MT4 EXNESS (Login: 70559995)
- MT5 EXNESS (Login: 279260115)

✅ **Python Systems**
- Python Management System
- GenX-FX Trading System

✅ **Development Tools**
- Cursor IDE
- Chrome with trading dashboards
- Task Manager

✅ **Security**
- Desktop auto-lock after startup

---

## Troubleshooting

### Nothing happens after login?
1. Press `Win + R` → type `shell:startup` → Enter
2. Check if `A6-9V_Trading_System.lnk` exists
3. If missing, run `Install_AutoStartup.bat` → Option 1

### System starts but some components fail?
1. Test manually: Double-click `A6-9V_Enhanced_Master_Launcher.bat`
2. Look for specific error messages
3. Check file paths in the batch file

### Don't want auto-startup anymore?
1. Run `Install_AutoStartup.bat`
2. Select option **2** (Uninstall)
3. Confirm removal

---

## File Locations

All files in: `C:\Users\lengk\Dropbox\OneDrive\Desktop\`
- `A6-9V_Enhanced_Master_Launcher.bat` (Main launcher)
- `A6-9V_Silent_Launcher.vbs` (Silent starter)
- `Install_AutoStartup.bat` (Setup tool)

Startup shortcut: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`

---

## Important Notes

⚠️ **First Time Setup**
- Run the installation script ONCE
- Test before relying on it
- Verify all components start correctly

⚠️ **Security**
- Desktop locks automatically (15 seconds after startup)
- Trading credentials are in the batch files
- Ensure proper file permissions

⚠️ **Performance**
- Full startup takes ~2 minutes
- CPU usage may spike temporarily
- Normal operation resumes quickly

---

## Need More Help?

📖 **Full Documentation**: `WINDOWS_AUTO_STARTUP_GUIDE.md`
📊 **System Info**: `A6-9V_Master_System_README.md`

---

**Organization: A6-9V | Quick Reference Card**
**Status: OPERATIONAL** ✅
