@echo off
REM Setup Jules Communication Environment Variables
REM GenX_FX Trading Platform - Multi-Agent Communication

echo Setting up Jules Communication Environment...

REM Load Jules communication settings
for /f "delims=" %%x in (jules_communication.env) do (set "%%x")

REM Set system environment variables
setx JULES_HTTP_PORT %JULES_HTTP_PORT%
setx JULES_API_HOST %JULES_API_HOST%
setx JULES_API_URL %JULES_API_URL%
setx MULTI_AGENT_GATEWAY_PORT %MULTI_AGENT_GATEWAY_PORT%
setx MULTI_AGENT_GATEWAY_URL %MULTI_AGENT_GATEWAY_URL%

echo.
echo Jules Communication Environment Setup Complete!
echo.
echo Key Settings:
echo - Jules HTTP Port: %JULES_HTTP_PORT%
echo - API URL: %JULES_API_URL%
echo - Gateway Port: %MULTI_AGENT_GATEWAY_PORT%
echo - Health Check: %HEALTH_CHECK_URL%
echo.
echo Environment variables have been set for the current session and saved permanently.
echo.
pause