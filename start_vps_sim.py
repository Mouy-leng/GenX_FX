
import sys
sys.path.append('D:\Dropbox\GenX_FX')

print('Starting GenX VPS Simulation...')

try:
    from api.fastapi_server import app
    import uvicorn
    print('Modules imported successfully')
    print('Starting server on http://localhost:8001')
    uvicorn.run(app, host='0.0.0.0', port=8001, log_level='info')
except Exception as e:
    print(f'Startup error: {e}')
    import traceback
    traceback.print_exc()
