import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class FXCMForexConnectConfig:
    """Credentials for FXCM ForexConnect API"""
    username: str = field(default_factory=lambda: os.getenv('FXCM_USERNAME'))
    password: str = field(default_factory=lambda: os.getenv('FXCM_PASSWORD'))
    connection_type: str = field(default_factory=lambda: os.getenv('FXCM_CONNECTION_TYPE', 'Demo'))
    url: str = field(default_factory=lambda: os.getenv('FXCM_URL', 'http://fxcorporate.com/Hosts.jsp'))

@dataclass
class FXCMConfig:
    """Credentials for FXCM REST/WebSocket API"""
    access_token: str = field(default_factory=lambda: os.getenv('FXCM_API_TOKEN'))
    environment: str = field(default_factory=lambda: os.getenv('FXCM_ENVIRONMENT', 'demo'))
    server_url: str = field(default_factory=lambda: os.getenv('FXCM_SERVER_URL', 'https://api-fxpractice.fxcm.com'))
    socket_url: str = field(default_factory=lambda: os.getenv('FXCM_SOCKET_URL', 'wss://api-fxpractice.fxcm.com/socket.io/'))

def get_fxcm_forexconnect_config() -> FXCMForexConnectConfig:
    """Returns a configuration object for the FXCM ForexConnect provider."""
    return FXCMForexConnectConfig()

def get_fxcm_config() -> FXCMConfig:
    """Returns a configuration object for the FXCM REST/WebSocket provider."""
    return FXCMConfig()