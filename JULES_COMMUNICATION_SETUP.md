# Jules Multi-Agent Communication Setup

## Overview
This document provides the complete setup for Jules multi-agent communication with the GenX_FX Trading Platform.

## HTTP Port Configuration

### Primary Communication Port
- **Jules HTTP Port**: `8080`
- **API Base URL**: `http://localhost:8080`
- **Protocol**: HTTP/HTTPS
- **Format**: JSON

### Network Architecture
Based on the current working setup from `network_map.md`:

```
genx-fx-working    -> Port 8080 (Trading API)
genxdb_fx_redis    -> Port 6379 (Cache)
genxdb_fx_mysql    -> Port 3306 (Database)
genxdb_fx_monitoring -> Port 3001 (Grafana)
```

## API Endpoints for Jules Communication

### Core Endpoints
- **Health Check**: `http://localhost:8080/health`
- **Agent Status**: `http://localhost:8080/agent/status`
- **Trading Signals**: `http://localhost:8080/trading/signals`
- **Place Orders**: `http://localhost:8080/trading/orders`

### Signal Endpoints
- **MT4 Signals**: `http://localhost:8080/MT4_Signals.csv`
- **MT5 Signals**: `http://localhost:8080/MT5_Signals.csv`
- **JSON Signals**: `http://localhost:8080/signals/json`

## Environment Setup

### 1. Load Environment Variables
Run one of the following scripts to set up the environment:

**Windows Batch:**
```cmd
setup_jules_env.bat
```

**PowerShell:**
```powershell
.\setup_jules_env.ps1
```

### 2. Verify Environment
Check that the following variables are set:
- `JULES_HTTP_PORT=8080`
- `JULES_API_URL=http://localhost:8080`
- `MULTI_AGENT_GATEWAY_PORT=8080`

### 3. Test Connection
```bash
curl http://localhost:8080/health
```

## Jules Plugin Configuration

### Plugin Location
- **Path**: `./genx-cli/plugins/jules_plugin.js`
- **Config**: `.julenrc`

### Plugin Settings
```json
{
  "plugins": [
    "jules_plugin",
    "codacy_plugin",
    "license_checker.py",
    "amp_adapter",
    "historymaker_plugin"
  ]
}
```

## Multi-Agent Communication Flow

### 1. Agent Registration
Jules agents register with the gateway using device authentication:
```
POST /auth/device/session
Headers: X-Device-ID: genx-fx-jules-agent
```

### 2. Status Monitoring
Agents report status periodically:
```
GET /agent/status
```

### 3. Signal Processing
Agents can retrieve and process trading signals:
```
GET /trading/signals
GET /signals/json
```

### 4. Order Management
Agents can place and manage orders:
```
POST /trading/orders
GET /trading/orders/{order_id}
DELETE /trading/orders/{order_id}
```

## Security Configuration

### Device Authentication
- **Required**: Yes
- **Device ID**: `genx-fx-jules-agent`
- **Method**: Header-based authentication

### API Security
- **CORS**: Enabled for all origins
- **Authentication**: Firebase-based user auth + device auth
- **Rate Limiting**: Configured per endpoint

## Troubleshooting

### Common Issues
1. **Port 8080 in use**: Check if Docker container is running
2. **Connection refused**: Verify API server is started
3. **Authentication failed**: Check device ID configuration

### Verification Commands
```bash
# Check if port is open
netstat -an | findstr :8080

# Test API health
curl http://localhost:8080/health

# Check Docker containers
docker ps | findstr genx-fx
```

## Integration Examples

### Python Example
```python
import requests
import os

# Load environment variables
jules_port = os.getenv('JULES_HTTP_PORT', '8080')
api_url = os.getenv('JULES_API_URL', f'http://localhost:{jules_port}')

# Test connection
response = requests.get(f'{api_url}/health')
print(f"API Status: {response.json()}")

# Get trading signals
signals = requests.get(f'{api_url}/trading/signals')
print(f"Active Signals: {signals.json()}")
```

### JavaScript Example
```javascript
const julesPort = process.env.JULES_HTTP_PORT || '8080';
const apiUrl = process.env.JULES_API_URL || `http://localhost:${julesPort}`;

// Test connection
fetch(`${apiUrl}/health`)
  .then(response => response.json())
  .then(data => console.log('API Status:', data));

// Get trading signals
fetch(`${apiUrl}/trading/signals`)
  .then(response => response.json())
  .then(signals => console.log('Active Signals:', signals));
```

## Next Steps

1. ✅ Environment variables configured
2. ✅ HTTP port (8080) identified and documented
3. ✅ API endpoints mapped for Jules communication
4. 🔄 Test Jules agent connection
5. 🔄 Implement multi-agent coordination
6. 🔄 Set up monitoring and logging

## Support

For issues with Jules communication setup:
1. Check the logs in `./logs/jules_communication.log`
2. Verify Docker containers are running
3. Test API endpoints manually
4. Review network configuration in `network_map.md`