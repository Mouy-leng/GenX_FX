"""
WebSocket Service for real-time data streaming
"""

import asyncio
import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class WebSocketService:
    """WebSocket service for real-time data"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.connections = set()
        self.is_running = False
        
        logger.info("WebSocket Service initialized")
    
    async def start(self, host: str = 'localhost', port: int = 8080):
        """Start the WebSocket service"""
        try:
            self.is_running = True
            logger.info(f"WebSocket service started on {host}:{port}")
        except Exception as e:
            logger.error(f"Failed to start WebSocket service: {e}")
            raise
    
    async def stop(self):
        """Stop the WebSocket service"""
        self.is_running = False
        logger.info("WebSocket service stopped")
    
    async def broadcast_signal(self, signal_data: Dict[str, Any]):
        """Broadcast signal to all connected clients"""
        try:
            message = json.dumps(signal_data)
            for connection in self.connections:
                try:
                    await connection.send(message)
                except Exception as e:
                    logger.error(f"Error sending message to client: {e}")
                    self.connections.discard(connection)
        except Exception as e:
            logger.error(f"Error broadcasting signal: {e}")
