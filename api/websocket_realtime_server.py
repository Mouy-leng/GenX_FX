#!/usr/bin/env python3
"""
GenX Advanced WebSocket Server - Real-time Trading Updates
Provides WebSocket connections for live trading data streaming
"""

import asyncio
import json
import logging
from datetime import datetime
import websockets
from websockets.server import serve
import aiohttp
from typing import Set

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connected clients
connected_clients: Set = set()

async def get_trading_data():
    """Fetch latest trading data from FastAPI server"""
    try:
        async with aiohttp.ClientSession() as session:
            # Get signals
            async with session.get("http://localhost:8000/signals", timeout=3) as response:
                if response.status == 200:
                    signals_data = await response.json()
                else:
                    signals_data = {"signals": [], "error": "FastAPI unavailable"}
            
            # Get portfolio
            async with session.get("http://localhost:8000/portfolio", timeout=3) as response:
                if response.status == 200:
                    portfolio_data = await response.json()
                else:
                    portfolio_data = {"data": {"balance": 0}, "error": "Portfolio unavailable"}
            
            # Get stats
            async with session.get("http://localhost:8000/stats", timeout=3) as response:
                if response.status == 200:
                    stats_data = await response.json()
                else:
                    stats_data = {"error": "Stats unavailable"}
            
            return {
                "type": "trading_update",
                "timestamp": datetime.now().isoformat(),
                "signals": signals_data.get("signals", []),
                "portfolio": portfolio_data.get("data", {}),
                "stats": stats_data,
                "clients_connected": len(connected_clients)
            }
    except Exception as e:
        logger.error(f"Error fetching trading data: {e}")
        return {
            "type": "error",
            "message": f"Failed to fetch data: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

async def handle_client(websocket, path):
    """Handle individual WebSocket client connections"""
    client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    logger.info(f"Client connected: {client_id}")
    
    # Add client to connected set
    connected_clients.add(websocket)
    
    try:
        # Send welcome message
        welcome_message = {
            "type": "welcome",
            "message": "Connected to GenX Trading WebSocket",
            "client_id": client_id,
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send(json.dumps(welcome_message))
        
        # Handle incoming messages
        async for message in websocket:
            try:
                data = json.loads(message)
                command = data.get("command", "")
                
                if command == "get_signals":
                    trading_data = await get_trading_data()
                    await websocket.send(json.dumps(trading_data))
                    
                elif command == "subscribe":
                    # Client wants real-time updates
                    response = {
                        "type": "subscription_confirmed",
                        "message": "Subscribed to real-time updates",
                        "timestamp": datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(response))
                    
                elif command == "ping":
                    # Heartbeat
                    pong = {
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(pong))
                    
                else:
                    # Unknown command
                    error_response = {
                        "type": "error",
                        "message": f"Unknown command: {command}",
                        "timestamp": datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(error_response))
                    
            except json.JSONDecodeError:
                error_response = {
                    "type": "error",
                    "message": "Invalid JSON message",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(error_response))
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client disconnected: {client_id}")
    except Exception as e:
        logger.error(f"Error handling client {client_id}: {e}")
    finally:
        # Remove client from connected set
        connected_clients.discard(websocket)
        logger.info(f"Client {client_id} cleaned up. Connected clients: {len(connected_clients)}")

async def broadcast_updates():
    """Broadcast trading updates to all connected clients"""
    while True:
        try:
            if connected_clients:
                # Get latest trading data
                trading_data = await get_trading_data()
                
                # Broadcast to all connected clients
                if connected_clients:
                    message = json.dumps(trading_data)
                    disconnected = set()
                    
                    for client in connected_clients.copy():
                        try:
                            await client.send(message)
                        except websockets.exceptions.ConnectionClosed:
                            disconnected.add(client)
                        except Exception as e:
                            logger.error(f"Error sending to client: {e}")
                            disconnected.add(client)
                    
                    # Remove disconnected clients
                    for client in disconnected:
                        connected_clients.discard(client)
                    
                    if trading_data.get("type") != "error":
                        logger.info(f"Broadcasted update to {len(connected_clients)} clients")
            
        except Exception as e:
            logger.error(f"Error in broadcast loop: {e}")
        
        # Wait 10 seconds before next broadcast
        await asyncio.sleep(10)

async def start_websocket_server():
    """Start the WebSocket server"""
    logger.info("Starting GenX WebSocket Server on port 8765...")
    
    # Start broadcast task
    broadcast_task = asyncio.create_task(broadcast_updates())
    
    try:
        # Start WebSocket server
        async with serve(handle_client, "0.0.0.0", 8765):
            logger.info("WebSocket server started on ws://0.0.0.0:8765")
            logger.info("Phone access: ws://10.124.54.249:8765")
            
            # Keep server running
            await asyncio.Future()  # run forever
            
    except Exception as e:
        logger.error(f"WebSocket server error: {e}")
        broadcast_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(start_websocket_server())
    except KeyboardInterrupt:
        logger.info("WebSocket server stopped by user")
    except Exception as e:
        logger.error(f"Server startup error: {e}")