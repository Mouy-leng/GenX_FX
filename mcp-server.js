#!/usr/bin/env node

/**
 * GenX Trading MCP Server
 * Provides access to trading bot status, signals, and configuration
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const net = require('net');

class GenXTradingMCPServer {
    constructor() {
        this.telegramBotToken = process.env.TELEGRAM_BOT_TOKEN;
        this.telegramUserId = process.env.TELEGRAM_USER_ID;
        this.telegramGroupId = process.env.TELEGRAM_GROUP_ID;
        this.apiBaseUrl = process.env.API_BASE_URL || 'http://127.0.0.1:8080';
        this.eaServerHost = process.env.EA_SERVER_HOST || 'localhost';
        this.eaServerPort = process.env.EA_SERVER_PORT || '9090'; this.tools = [
            {
                name: "get_bot_status",
                description: "Get current status of the Telegram trading bot",
                inputSchema: {
                    type: "object",
                    properties: {},
                    required: []
                }
            },
            {
                name: "send_telegram_message",
                description: "Send a message via Telegram bot",
                inputSchema: {
                    type: "object",
                    properties: {
                        message: { type: "string", description: "Message to send" },
                        chat_id: { type: "string", description: "Chat ID (optional, defaults to configured user)" }
                    },
                    required: ["message"]
                }
            },
            {
                name: "get_trading_signals",
                description: "Get current trading signals from the AI system",
                inputSchema: {
                    type: "object",
                    properties: {
                        symbol: { type: "string", description: "Trading symbol (optional)" },
                        limit: { type: "number", description: "Number of signals to return" }
                    },
                    required: []
                }
            },
            {
                name: "get_server_info",
                description: "Get information about running servers and their status",
                inputSchema: {
                    type: "object",
                    properties: {},
                    required: []
                }
            },
            {
                name: "check_ea_connection",
                description: "Check connection status to MetaTrader EA",
                inputSchema: {
                    type: "object",
                    properties: {},
                    required: []
                }
            },
            {
                name: "get_phone_debug_info",
                description: "Get debugging information for phone connection to bot",
                inputSchema: {
                    type: "object",
                    properties: {},
                    required: []
                }
            }
        ];
    }

    async handleTool(name, args) {
        try {
            switch (name) {
                case "get_bot_status":
                    return await this.getBotStatus();
                case "send_telegram_message":
                    return await this.sendTelegramMessage(args.message, args.chat_id);
                case "get_trading_signals":
                    return await this.getTradingSignals(args.symbol, args.limit);
                case "get_server_info":
                    return await this.getServerInfo();
                case "check_ea_connection":
                    return await this.checkEAConnection();
                case "get_phone_debug_info":
                    return await this.getPhoneDebugInfo();
                default:
                    throw new Error(`Unknown tool: ${name}`);
            }
        } catch (error) {
            return {
                isError: true,
                content: [{
                    type: "text",
                    text: `Error executing ${name}: ${error.message}`
                }]
            };
        }
    }

    async getBotStatus() {
        try {
            const response = await fetch(`https://api.telegram.org/bot${this.telegramBotToken}/getMe`);
            const data = await response.json();

            if (data.ok) {
                return {
                    content: [{
                        type: "text",
                        text: `✅ Telegram Bot Active\\n\\nBot Info:\\n- Username: @${data.result.username}\\n- Name: ${data.result.first_name}\\n- ID: ${data.result.id}\\n- Can Join Groups: ${data.result.can_join_groups}\\n- Can Read Messages: ${data.result.can_read_all_group_messages}`
                    }]
                };
            } else {
                throw new Error(`Telegram API error: ${data.description}`);
            }
        } catch (error) {
            return {
                isError: true,
                content: [{
                    type: "text",
                    text: `❌ Bot Status Check Failed: ${error.message}`
                }]
            };
        }
    }

    async sendTelegramMessage(message, chatId = null) {
        try {
            const targetChatId = chatId || this.telegramUserId;
            const url = `https://api.telegram.org/bot${this.telegramBotToken}/sendMessage`;

            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chat_id: targetChatId,
                    text: message,
                    parse_mode: 'Markdown'
                })
            });

            const data = await response.json();

            if (data.ok) {
                return {
                    content: [{
                        type: "text",
                        text: `✅ Message sent successfully to chat ${targetChatId}`
                    }]
                };
            } else {
                throw new Error(`Telegram API error: ${data.description}`);
            }
        } catch (error) {
            return {
                isError: true,
                content: [{
                    type: "text",
                    text: `❌ Failed to send message: ${error.message}`
                }]
            };
        }
    }

    async getTradingSignals(symbol = null, limit = 10) {
        try {
            let url = `${this.apiBaseUrl}/api/signals`;
            const params = new URLSearchParams();

            if (symbol) params.append('symbol', symbol);
            if (limit) params.append('limit', limit.toString());

            if (params.toString()) {
                url += `?${params.toString()}`;
            }

            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`API returned ${response.status}: ${response.statusText}`);
            }

            const signals = await response.json();

            return {
                content: [{
                    type: "text",
                    text: `📊 Trading Signals (${signals.length} found):\\n\\n${signals.map(signal =>
                        `Symbol: ${signal.symbol}\\nAction: ${signal.action}\\nEntry: ${signal.entry_price}\\nTarget: ${signal.target_price}\\nStop Loss: ${signal.stop_loss}\\nConfidence: ${signal.confidence}%\\n---`
                    ).join('\\n')}`
                }]
            };
        } catch (error) {
            return {
                isError: true,
                content: [{
                    type: "text",
                    text: `❌ Failed to get trading signals: ${error.message}`
                }]
            };
        }
    }

    async getServerInfo() {
        const serverChecks = [
            { name: 'API Server', host: '127.0.0.1', port: 8080 },
            { name: 'FastAPI Server', host: '127.0.0.1', port: 8000 },
            { name: 'EA Communication Server', host: this.eaServerHost, port: parseInt(this.eaServerPort) },
            { name: 'Frontend Server', host: '127.0.0.1', port: 5173 }
        ];

        const results = await Promise.all(
            serverChecks.map(server => this.checkPort(server.host, server.port, server.name))
        );

        return {
            content: [{
                type: "text",
                text: `🖥️ Server Status Report:\\n\\n${results.join('\\n')}`
            }]
        };
    }

    checkPort(host, port, name) {
        return new Promise((resolve) => {
            const socket = new net.Socket();
            const timeout = 3000;

            socket.setTimeout(timeout);

            socket.on('connect', () => {
                socket.destroy();
                resolve(`✅ ${name} (${host}:${port}) - ONLINE`);
            });

            socket.on('timeout', () => {
                socket.destroy();
                resolve(`⏰ ${name} (${host}:${port}) - TIMEOUT`);
            });

            socket.on('error', () => {
                resolve(`❌ ${name} (${host}:${port}) - OFFLINE`);
            });

            socket.connect(port, host);
        });
    }

    async checkEAConnection() {
        try {
            const isConnected = await this.checkPort(this.eaServerHost, parseInt(this.eaServerPort), 'EA Server');

            return {
                content: [{
                    type: "text",
                    text: `🔌 MetaTrader EA Connection Status:\\n\\n${isConnected}\\n\\nConnection Details:\\n- Host: ${this.eaServerHost}\\n- Port: ${this.eaServerPort}\\n- Protocol: TCP Socket`
                }]
            };
        } catch (error) {
            return {
                isError: true,
                content: [{
                    type: "text",
                    text: `❌ EA Connection Check Failed: ${error.message}`
                }]
            };
        }
    }

    async getPhoneDebugInfo() {
        const debugInfo = {
            telegramBot: {
                token: this.telegramBotToken ? '✅ Configured' : '❌ Missing',
                userId: this.telegramUserId ? '✅ Configured' : '❌ Missing'
            },
            serverEndpoints: {
                api: `${this.apiBaseUrl}`,
                ea: `${this.eaServerHost}:${this.eaServerPort}`
            },
            phoneAccessMethods: [
                '📱 Telegram Bot - Direct messaging',
                '🌐 Web Interface - Browser access',
                '🔌 API Endpoints - Direct API calls',
                '📡 WebSocket - Real-time updates'
            ],
            troubleshooting: [
                '1. Check if bot responds to /start command',
                '2. Verify user ID in bot logs',
                '3. Test API endpoints from phone browser',
                '4. Check network connectivity to server'
            ]
        };

        return {
            content: [{
                type: "text",
                text: `📱 Phone Debug Information:\\n\\n**Bot Configuration:**\\n- Token: ${debugInfo.telegramBot.token}\\n- User ID: ${debugInfo.telegramBot.userId}\\n\\n**Server Endpoints:**\\n- API: ${debugInfo.serverEndpoints.api}\\n- EA: ${debugInfo.serverEndpoints.ea}\\n\\n**Access Methods:**\\n${debugInfo.phoneAccessMethods.join('\\n')}\\n\\n**Troubleshooting Steps:**\\n${debugInfo.troubleshooting.join('\\n')}`
            }]
        };
    }

    async start() {
        // Standard MCP server initialization
        console.log(JSON.stringify({
            jsonrpc: "2.0",
            method: "notifications/initialized",
            params: {}
        }));

        // Handle incoming requests
        process.stdin.on('data', async (data) => {
            try {
                const request = JSON.parse(data.toString());

                if (request.method === "tools/list") {
                    console.log(JSON.stringify({
                        jsonrpc: "2.0",
                        id: request.id,
                        result: { tools: this.tools }
                    }));
                } else if (request.method === "tools/call") {
                    const result = await this.handleTool(request.params.name, request.params.arguments || {});
                    console.log(JSON.stringify({
                        jsonrpc: "2.0",
                        id: request.id,
                        result
                    }));
                }
            } catch (error) {
                console.log(JSON.stringify({
                    jsonrpc: "2.0",
                    id: request.id || null,
                    error: {
                        code: -32603,
                        message: "Internal error",
                        data: error.message
                    }
                }));
            }
        });
    }
}

// Start the server
const server = new GenXTradingMCPServer();
server.start();