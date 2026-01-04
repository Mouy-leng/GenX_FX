# MT5 Expert Advisors Configuration - Quick Reference

## Organization: A6-9V | Exness-MT5Trial8 Demo Account

---

## 📊 Account Information

| Property | Value |
|----------|-------|
| **Account Name** | Exness-MT5Trial8 |
| **Account Type** | Demo (Hedging) |
| **Login** | 279260115 |
| **Server** | Exness-MT5Trail8 |
| **Balance** | 39,499.31 USD |
| **Equity** | 39,499.31 USD |
| **Free Margin** | 39,499.31 USD |
| **Description** | "Im Good only for testing" |

---

## 🤖 Expert Advisors List

### Primary Trading Systems

| EA Name | Type | Purpose |
|---------|------|---------|
| **ExpertMAPSAR_Enhanced** | Enhanced | Advanced Parabolic SAR with optimizations |
| **ExpertMAPSAR Enhanced** | Enhanced | Alternative enhanced version |
| **ExpertMAPSARSizeOptimized** | Optimized | Position size and risk management optimized |
| **ExpertMAPSAR** | Standard | Basic Parabolic SAR implementation |

### Additional Trading Systems

| EA Name | Type | Purpose |
|---------|------|---------|
| **ExpertMACD** | Indicator-based | MACD crossover strategy |
| **ExpertMAMA** | Adaptive | MESA Adaptive Moving Average |
| **bridges3rd** | Bridge/Utility | Connection/bridge functionality |
| **Advisors_backup_20251226_235613** | Backup | Configuration backup from Dec 26, 2025 |

---

## 💹 Market Watch Symbols

### Primary Forex Pairs
- **EURUSD** - Euro vs US Dollar
- **USDJPY** - US Dollar vs Japanese Yen
- **GBPUSD** - British Pound vs US Dollar
- **GBPJPY** - British Pound vs Japanese Yen
- **USDCAD** - US Dollar vs Canadian Dollar
- **USDCHF** - US Dollar vs Swiss Franc

### Precious Metals
- **XAUUSD** - Gold vs US Dollar (Popular for trading)

### Cryptocurrencies
- **BTCUSD** - Bitcoin vs US Dollar
- **ETHUSD** - Ethereum vs US Dollar
- **BTCCNH** - Bitcoin vs Chinese Yuan
- **BTCXAU** - Bitcoin vs Gold
- **BTCZAR** - Bitcoin vs South African Rand

### Exotic Pairs
- **USDARS** - US Dollar vs Argentine Peso

---

## ⚡ Quick Launch Commands

### Windows PowerShell

```powershell
# Launch MT5 with automated login
powershell -ExecutionPolicy Bypass -File "MT_AutoLogin_Fixed.ps1" -Platform mt5

# Enable Expert Advisors
powershell -ExecutionPolicy Bypass -File "Enable_MT_AutoTrading.ps1"

# Full system launch
.\A6-9V_Enhanced_Master_Launcher.bat
```

### Manual MT5 Shortcuts

| Action | Keyboard Shortcut |
|--------|------------------|
| Open Login Dialog | Ctrl + O |
| Enable Expert Advisors | Ctrl + E |
| New Chart | Ctrl + N |
| Market Watch | Ctrl + M |
| Navigator | Ctrl + N |
| Terminal | Ctrl + T |

---

## ✅ Verification Checklist

### Visual Indicators

- [ ] **Title Bar** shows: "Exness-MT5Trial8" with "Demo" and "Hedging" labels
- [ ] **Connection Status** displays: "Exness-MT5Trail8" (bottom right)
- [ ] **AutoTrading Button** is GREEN (toolbar, top)
- [ ] **Balance Display** shows: "39,499.31 USD" (bottom panel)

### Navigator Panel

- [ ] **Accounts** section visible on left
- [ ] **Exness-MT5Real8** listed (not active)
- [ ] **Exness-MT5Trial8** highlighted/active
- [ ] Description shows: "Im Good only for testing"

### Expert Advisors

- [ ] All 8 EAs listed in Navigator
- [ ] Expert Advisors folder expanded
- [ ] EAs can be dragged to charts
- [ ] "Expert Advisors" tab in Terminal window

### Market Watch

- [ ] Symbols list visible on left panel
- [ ] Bid/Ask prices updating in real-time
- [ ] Daily change % shown for each symbol
- [ ] All primary symbols (XAUUSD, BTCUSD, EURUSD, etc.) listed

---

## 🔧 Enable AutoTrading - Step by Step

### Method 1: Keyboard Shortcut (Fastest)
1. Click on MT5 window to focus it
2. Press **Ctrl + E**
3. Verify AutoTrading button turns green

### Method 2: Toolbar Button
1. Look for "AutoTrading" button in toolbar
2. Click the button (it will turn green when active)
3. Verify status in Terminal → Expert Advisors tab

### Method 3: PowerShell Script (Automated)
```powershell
powershell -ExecutionPolicy Bypass -File "Enable_MT_AutoTrading.ps1"
```

### Method 4: Options Menu
1. Go to **Tools → Options** (Ctrl + O)
2. Click **Expert Advisors** tab
3. Check the following:
   - ✅ Allow automated trading
   - ✅ Allow DLL imports
   - ✅ Allow WebRequest for listed URL
4. Click **OK**
5. Enable AutoTrading button in toolbar

---

## 🎯 EA Attachment to Charts

### How to Attach an Expert Advisor:

1. **Open Navigator** (Ctrl + N)
2. **Expand Expert Advisors** folder
3. **Drag desired EA** (e.g., ExpertMAPSAR_Enhanced) to chart
4. **Configuration Dialog** appears:
   - Set parameters (lot size, stop loss, take profit, etc.)
   - Check "Allow live trading"
   - Check "Allow DLL imports" (if required)
5. **Click OK**
6. **Verify** smiley face appears in top-right corner of chart:
   - 😊 = EA is happy and trading
   - 😐 = EA is loaded but AutoTrading disabled
   - ❌ = EA has error or stopped

---

## 📈 Trading Status Indicators

### Connection Status Colors
- **Green** = Connected to server
- **Red** = Disconnected
- **Yellow** = Attempting to connect

### AutoTrading Button States
- **Green** = AutoTrading ENABLED (EAs can trade)
- **Red/Gray** = AutoTrading DISABLED (EAs cannot trade)

### Chart EA Face Indicators
- **😊 Smiley** = EA active and can trade
- **😐 Neutral** = EA loaded but AutoTrading off
- **❌ Cross** = EA error or disabled

---

## 🛠️ Common Troubleshooting

### Issue: AutoTrading Button Won't Turn Green

**Solutions:**
1. Restart MT5 platform
2. Check Tools → Options → Expert Advisors settings
3. Verify EA is properly configured on chart
4. Check if EA requires specific permissions

### Issue: EA Shows ❌ on Chart

**Solutions:**
1. Right-click chart → Expert Advisors → Properties
2. Check "Allow live trading" is enabled
3. Verify EA parameters are valid
4. Check Experts log for error messages (View → Toolbox → Experts)

### Issue: Symbols Not in Market Watch

**Solutions:**
1. Right-click Market Watch → Show All
2. Right-click Market Watch → Symbols
3. Search for symbol (e.g., XAUUSD)
4. Right-click symbol → Show

### Issue: Balance Not Updating

**Solutions:**
1. Check internet connection
2. Verify connection status (bottom-right)
3. Re-login if necessary (Ctrl + O)
4. Check if demo account is still active

---

## 📞 Quick Access Information

### Account Management
- **Demo Account:** Exness-MT5Trial8 (Current)
- **Live Account:** Exness-MT5Real8 (Available for production)
- **Switch Accounts:** File → Login to Trade Account

### Support Resources
- **Launch Guide:** `REPOSITORY_LAUNCH_GUIDE.md`
- **System README:** `A6-9V_Master_System_README.md`
- **Credential Setup:** `AUTONOMOUS_CREDENTIAL_SETUP.md`

### Web Resources
- **Code With Me:** https://code-with-me.global.jetbrains.com/ZhaX8frcoZS0qveUMv8vAg
- **TradingView:** https://www.tradingview.com
- **Yahoo Finance:** https://finance.yahoo.com

---

## 🚨 Pre-Trading Safety Checklist

Before activating any Expert Advisor for live trading:

- [ ] Test on demo account first (current: Exness-MT5Trial8) ✅
- [ ] Verify EA settings (lot size, stop loss, take profit)
- [ ] Set maximum daily loss limit
- [ ] Configure risk management parameters
- [ ] Test on multiple timeframes and symbols
- [ ] Monitor EA performance for at least 1 week
- [ ] Review trading logs and statistics
- [ ] Ensure sufficient account balance
- [ ] Verify internet connection stability
- [ ] Have backup plan for connection loss

---

## 💡 Pro Tips

1. **Start Small:** Begin with minimum lot sizes when testing EAs
2. **Monitor Regularly:** Check EA performance at least daily
3. **Keep Logs:** Save EA logs and performance reports
4. **Backup Settings:** Export EA configurations regularly
5. **Update EAs:** Keep Expert Advisors updated to latest versions
6. **Diversify:** Don't rely on a single EA or strategy
7. **Stay Informed:** Monitor economic calendar for high-impact events
8. **Risk Management:** Never risk more than 2% of account per trade

---

**🎯 Organization: A6-9V | Status: READY FOR TESTING**

*Last Updated: 2026-01-04*
