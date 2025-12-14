# 🚀 A6-9V Windows Auto-Startup Setup Guide

## Organization: A6-9V
**Automated Trading System - Windows Startup Configuration**

---

## 📋 Overview

This guide explains how to configure your Windows laptop to automatically launch the A6-9V Enhanced Master Trading System when you log in. This ensures your trading platforms, Python systems, and development tools start automatically without manual intervention.

**⚠️ Note on File Paths:** This guide uses the default installation directory `C:\Users\lengk\Dropbox\OneDrive\Desktop\`. If your files are in a different location, replace this path with your actual directory path throughout this guide.

---

## ✨ Features

- ✅ **Silent Background Launch** - System starts without showing console windows
- ✅ **One-Click Installation** - Automated setup script
- ✅ **Easy Management** - Install, uninstall, or check status anytime
- ✅ **Safe & Secure** - Uses standard Windows Startup folder
- ✅ **No Admin Required** - Runs with your user permissions

---

## 📁 Required Files

The auto-startup system consists of three main files:

1. **A6-9V_Silent_Launcher.vbs** - VBScript that launches the system silently
2. **Install_AutoStartup.bat** - Installation/management tool
3. **A6-9V_Enhanced_Master_Launcher.bat** - The main trading system launcher (already exists)

All files should be in the same directory (example shown, adjust to your actual path):
```
C:\Users\lengk\Dropbox\OneDrive\Desktop\
├── A6-9V_Enhanced_Master_Launcher.bat
├── A6-9V_Silent_Launcher.vbs
└── Install_AutoStartup.bat
```

---

## 🚀 Quick Start - Installation

### Method 1: Automated Installation (Recommended)

1. **Locate the Installation Script**
   - Navigate to: `C:\Users\lengk\Dropbox\OneDrive\Desktop\`
   - Find: `Install_AutoStartup.bat`

2. **Run the Installation**
   - Double-click `Install_AutoStartup.bat`
   - Select option **1** (Install Auto-Startup)
   - Press Enter

3. **Verify Installation**
   - The script will confirm successful installation
   - A shortcut will be created in your Windows Startup folder

4. **Test the Setup**
   - Option 1: Restart your computer and log in
   - Option 2: Run the VBScript manually to test: double-click `A6-9V_Silent_Launcher.vbs`

### Method 2: Manual Installation

If you prefer to set it up manually:

1. **Open Windows Startup Folder**
   - Press `Win + R` to open Run dialog
   - Type: `shell:startup`
   - Press Enter

2. **Create Shortcut**
   - Right-click in the Startup folder
   - Select `New > Shortcut`
   - Browse to: `C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V_Silent_Launcher.vbs`
   - Name it: `A6-9V_Trading_System`
   - Click Finish

3. **Verify**
   - The shortcut should appear in the Startup folder
   - Next login will automatically start the system

---

## 🔧 Management Options

### Check Auto-Startup Status

```batch
# Run Install_AutoStartup.bat and select option 3
```

This will show:
- ✅ Whether auto-startup is enabled or disabled
- 📁 Location of the startup shortcut
- 🎯 Target VBScript file path

### Uninstall Auto-Startup

```batch
# Run Install_AutoStartup.bat and select option 2
```

This will:
- ❌ Remove the startup shortcut
- 🔒 Stop the system from auto-starting
- ✅ Confirm successful removal

### Reinstall or Update

```batch
# Run Install_AutoStartup.bat and select option 1
# Confirm overwrite when prompted
```

---

## 🎯 What Happens on Startup?

When you log into Windows, the following sequence occurs:

### Phase 1: Silent Launch (Immediate)
- 🔇 VBScript runs silently in the background
- 🚀 Triggers the Enhanced Master Launcher

### Phase 2: MetaTrader Setup (0-30 seconds)
- 💹 MT4 EXNESS launches (Login: 70559995)
- 💹 MT5 EXNESS launches (Login: 279260115)
- ⏰ 15-second initialization wait
- 🔐 Automated login attempts (if script available)

### Phase 3: Core Systems (30-60 seconds)
- 📊 Python Management System starts
- 💹 GenX-FX Trading System initializes
- ✅ Virtual environments activate

### Phase 4: Development Tools (60-90 seconds)
- 🖥️ Cursor IDE opens
- 🌐 Chrome opens with trading dashboards
- 📈 Task Manager launches for monitoring

### Phase 5: Verification & Lock (90-120 seconds)
- 🔍 Process verification
- 🔒 Desktop auto-lock (after 15 seconds)

**Total Startup Time:** ~2 minutes from login to fully operational

---

## ⚙️ Configuration Options

### Disable Auto-Lock on Startup

If you don't want the desktop to auto-lock after startup:

1. Open: `A6-9V_Enhanced_Master_Launcher.bat`
2. Find these lines near the end:
   ```batch
   echo 🔒 Desktop will be locked in 15 seconds...
   timeout /t 15
   rundll32.exe user32.dll,LockWorkStation
   ```
3. Comment them out by adding `REM` at the start:
   ```batch
   REM echo 🔒 Desktop will be locked in 15 seconds...
   REM timeout /t 15
   REM rundll32.exe user32.dll,LockWorkStation
   ```

### Adjust Startup Delay

To add a delay before the system starts (useful if you need time to cancel):

1. Open: `A6-9V_Silent_Launcher.vbs`
2. Add this line before the `objShell.Run` command:
   ```vbscript
   WScript.Sleep 30000  ' Wait 30 seconds (30000 milliseconds)
   ```

### Change Launch Mode (Show Console Windows)

To see the console windows during startup (for debugging):

1. Open: `A6-9V_Silent_Launcher.vbs`
2. Change this line:
   ```vbscript
   objShell.Run """" & strBatchFile & """", 0, False
   ```
   To:
   ```vbscript
   objShell.Run """" & strBatchFile & """", 1, False
   ```
   (0 = hidden, 1 = normal window)

---

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### Issue 1: Nothing Happens on Startup

**Symptoms:** System doesn't start automatically after login

**Solutions:**
1. Check if shortcut exists:
   - Press `Win + R`
   - Type: `shell:startup`
   - Look for `A6-9V_Trading_System.lnk`

2. Verify VBScript location:
   - Open the shortcut properties
   - Confirm target path is correct

3. Test manually:
   - Double-click `A6-9V_Silent_Launcher.vbs`
   - Check if system starts

4. Check Windows Event Viewer:
   - Press `Win + X` → Event Viewer
   - Look under Windows Logs → Application

#### Issue 2: Error Message on Startup

**Symptoms:** Error popup: "A6-9V_Enhanced_Master_Launcher.bat not found"

**Solutions:**
1. Verify file locations:
   ```
   C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V_Enhanced_Master_Launcher.bat
   C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V_Silent_Launcher.vbs
   ```

2. If files moved, update paths:
   - Edit `A6-9V_Silent_Launcher.vbs`
   - Update `strBatchFile` path

3. Reinstall auto-startup:
   - Run `Install_AutoStartup.bat`
   - Select option 2 (Uninstall)
   - Then option 1 (Install)

#### Issue 3: MetaTrader Login Fails

**Symptoms:** MT4/MT5 launches but doesn't log in automatically

**Solutions:**
1. Verify PowerShell script exists:
   - Check: `MT_Login_Simple.ps1` or `MT_AutoLogin_Fixed.ps1`

2. Check PowerShell execution policy:
   ```powershell
   Get-ExecutionPolicy
   # Should be: RemoteSigned or Unrestricted
   ```

3. Set execution policy if needed:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. Verify credentials in the script:
   - Open PowerShell script
   - Check login, password, and server details

#### Issue 4: Python Systems Don't Start

**Symptoms:** MT4/MT5 launches but Python systems don't start

**Solutions:**
1. Check Python installation:
   ```batch
   C:\Users\lengk\AppData\Local\Programs\Python\Python313\python.exe --version
   ```

2. Verify Python script paths:
   - Check: `start_all.bat` exists
   - Check: `C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V\Trading\GenX_FX\main.py`

3. Test Python scripts manually:
   ```batch
   cd C:\Users\lengk\Dropbox\OneDrive\Desktop
   start_all.bat
   ```

#### Issue 5: High CPU Usage on Startup

**Symptoms:** Computer slows down significantly during startup

**Solutions:**
1. Add startup delays:
   - Edit `A6-9V_Enhanced_Master_Launcher.bat`
   - Increase `timeout` values between sections

2. Reduce simultaneous starts:
   - Comment out non-critical tools
   - Start them manually later

3. Close other programs:
   - Disable other startup programs temporarily
   - Use Task Manager → Startup tab

#### Issue 6: Desktop Locks Too Quickly

**Symptoms:** Desktop locks before you can intervene

**Solutions:**
1. Increase lock delay:
   - Edit `A6-9V_Enhanced_Master_Launcher.bat`
   - Change `timeout /t 15` to `timeout /t 60` (60 seconds)

2. Disable auto-lock:
   - See Configuration Options section above

### Disable Auto-Startup Temporarily

To prevent auto-startup for one session without uninstalling:

**Method 1:** Hold Shift during login
- Hold the Shift key while logging into Windows
- Keep holding until desktop appears
- Startup items will be skipped

**Method 2:** Disable in Task Manager
- Press `Ctrl + Shift + Esc`
- Go to Startup tab
- Find `A6-9V_Trading_System`
- Click Disable
- Re-enable when needed

---

## 🔐 Security Considerations

### Important Security Notes

1. **Credentials in Scripts**
   - ⚠️ Trading credentials are stored in batch/PowerShell files
   - 🔒 Ensure files have proper permissions
   - 💡 Consider encrypting sensitive files

2. **Auto-Lock Feature**
   - ✅ Desktop auto-locks after startup (default: 15 seconds)
   - 🔐 Protects your trading accounts
   - ⚙️ Can be disabled if needed (see Configuration Options)

3. **Unattended Operation**
   - ⚠️ System will trade automatically if configured
   - 📊 Ensure risk management is properly set
   - 👀 Monitor regularly

4. **File Access**
   - 🔒 Only your user account can access these files
   - 🛡️ No admin privileges required
   - 📁 Stored in your user directory

### Best Practices

1. **Test Before Production**
   - Test auto-startup on demo accounts first
   - Verify all systems start correctly
   - Monitor for errors or issues

2. **Regular Monitoring**
   - Check system logs daily
   - Review trading activity
   - Verify all components are running

3. **Backup Configuration**
   - Keep copies of all startup files
   - Document any customizations
   - Save credentials securely (encrypted)

4. **Update Regularly**
   - Keep Windows updated
   - Update MetaTrader platforms
   - Update Python packages

---

## 📊 Startup Verification Checklist

After installation, use this checklist to verify proper operation:

### Initial Setup
- [ ] `Install_AutoStartup.bat` runs successfully
- [ ] Auto-startup status shows "ENABLED"
- [ ] Shortcut exists in Startup folder
- [ ] VBScript file is accessible

### First Login Test
- [ ] System starts automatically after login
- [ ] MT4 EXNESS terminal launches
- [ ] MT5 EXNESS terminal launches
- [ ] Trading platforms show connection status
- [ ] Python Manager starts
- [ ] GenX-FX Trading System starts
- [ ] Cursor IDE opens
- [ ] Chrome opens with trading dashboards
- [ ] Task Manager displays
- [ ] Desktop locks (if enabled)

### Functionality Check
- [ ] MT4 shows server: Exness-Trail9
- [ ] MT5 shows server: Exness-MT5Trail8
- [ ] Account balances display correctly
- [ ] Expert Advisors are enabled
- [ ] Python systems are responsive
- [ ] No error messages or crashes

### Performance Check
- [ ] Total startup time < 3 minutes
- [ ] CPU usage returns to normal after startup
- [ ] Memory usage is acceptable
- [ ] No frozen or unresponsive windows

---

## 🔄 Updating the System

If you make changes to the launcher batch file or want to update the auto-startup:

1. **No Action Needed for Batch File Changes**
   - The VBScript points to the batch file
   - Any changes to the batch file are automatically used
   - No need to reinstall auto-startup

2. **Reinstalling After Moving Files**
   - If you move the directory, run:
   - `Install_AutoStartup.bat` → Option 2 (Uninstall)
   - `Install_AutoStartup.bat` → Option 1 (Install)

3. **Updating the VBScript**
   - Make changes to `A6-9V_Silent_Launcher.vbs`
   - Run: `Install_AutoStartup.bat` → Option 1
   - Confirm overwrite when prompted

---

## 📞 Support & Troubleshooting

### Log Files to Check

1. **Windows Event Viewer**
   ```
   Win + X → Event Viewer → Windows Logs → Application
   ```

2. **VBScript Errors**
   - Look for "Windows Script Host" errors
   - Check event description for details

3. **Batch File Output**
   - Modify VBScript to show window (see Configuration Options)
   - Review console output for errors

### Getting Help

If issues persist:

1. **Collect Information**
   - Screenshot of error messages
   - Check auto-startup status
   - Note what happens vs. what should happen

2. **Check File Locations**
   - Verify all files exist in expected locations
   - Check file permissions

3. **Test Components Individually**
   - Run VBScript manually
   - Run batch file manually
   - Test each component separately

---

## 🎯 Quick Reference

### File Locations

| File | Location |
|------|----------|
| Main Launcher | `C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V_Enhanced_Master_Launcher.bat` |
| Silent Launcher | `C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V_Silent_Launcher.vbs` |
| Install Tool | `C:\Users\lengk\Dropbox\OneDrive\Desktop\Install_AutoStartup.bat` |
| Startup Shortcut | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\A6-9V_Trading_System.lnk` |

### Quick Commands

| Action | Command |
|--------|---------|
| Open Startup Folder | `Win + R` → `shell:startup` |
| Check Status | Run `Install_AutoStartup.bat` → Option 3 |
| Disable Temporarily | Hold `Shift` during login |
| Test Manually | Double-click `A6-9V_Silent_Launcher.vbs` |

### Key Timeouts

| Phase | Duration |
|-------|----------|
| MT4/MT5 Launch Delay | 5 seconds each |
| Platform Initialization | 15 seconds |
| Component Delays | 2-3 seconds each |
| Auto-Lock Countdown | 15 seconds |
| **Total Startup Time** | **~2 minutes** |

---

## ✅ Success Indicators

Your auto-startup is working correctly if you see:

- ✅ MT4 terminal shows connection to Exness-Trail9
- ✅ MT5 terminal shows connection to Exness-MT5Trail8
- ✅ Python Manager window is running
- ✅ GenX-FX console is visible
- ✅ Cursor IDE is open
- ✅ Chrome shows trading dashboards
- ✅ Task Manager is monitoring processes
- ✅ No error messages or popups
- ✅ Desktop locks automatically (if enabled)

---

## 📈 Advanced Configuration

### Running as a Windows Service

For even more robust startup (survives logoff):

1. Use `windows_service_manager.py` (if available)
2. Configure as Windows Service
3. Set to auto-start with Windows

### Scheduled Task Alternative

Instead of Startup folder:

1. Open Task Scheduler
2. Create Task
3. Trigger: At logon
4. Action: Start program → `A6-9V_Silent_Launcher.vbs`
5. Conditions: Configure as needed

### Remote Monitoring

For monitoring startup from another device:

1. Enable remote desktop
2. Use RDP to connect and verify
3. Or: Set up monitoring alerts via email/SMS

---

**🚀 Organization: A6-9V | Auto-Startup System v1.0**

**Status: READY FOR DEPLOYMENT**

---

## 🎉 You're All Set!

Your A6-9V Enhanced Master Trading System is now configured for automatic startup. Your trading platform will launch every time you log into Windows, ensuring you never miss a trading opportunity.

**Happy Trading! 📈💹**
