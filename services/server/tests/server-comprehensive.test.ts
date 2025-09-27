import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import request from 'supertest';
import WebSocket, { WebSocketServer } from 'ws';
import express from 'express';
import { createServer } from 'http';
import cors from 'cors';

// Mock the routes and vite modules
vi.mock('../routes.js', () => ({
  registerRoutes: vi.fn((app) => {
    app.get('/api/test', (req, res) => res.json({ message: 'test endpoint' }));
    app.post('/api/data', (req, res) => res.json({ received: req.body }));
    app.get('/api/error', (req, res, next) => { next(new Error('Test error')); });
  })
}));

vi.mock('../vite.js', () => ({
  setupVite: vi.fn(),
  serveStatic: vi.fn()
}));

describe('GenX FX Server Comprehensive Tests', () => {
  let app: express.Application;
  let server: any;
  let wss: WebSocketServer;
  let serverAddress: string;

  beforeAll(async () => {
    app = express();
    
    app.use(cors({
      origin: ['http://localhost:3000', 'http://0.0.0.0:3000'],
      credentials: true
    }));

    app.use(express.json({ limit: '10mb' }));
    app.use(express.urlencoded({ extended: true }));

    app.get('/health', (req, res) => {
      res.json({ 
        status: 'OK', 
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'development'
      });
    });

    const { registerRoutes } = await import('../routes.js');
    registerRoutes(app);

    app.use((err: any, req: any, res: any, next: any) => {
      if (err instanceof SyntaxError && 'body' in err) {
        return res.status(400).json({ error: 'Malformed JSON' });
      }
      if (err.type === 'entity.too.large') {
        return res.status(413).json({ error: 'Payload Too Large' });
      }
      next(err);
    });

    app.use((err: any, req: any, res: any, next: any) => {
      res.status(500).json({
        error: 'Internal server error',
        message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
      });
    });

    app.use((req, res) => {
      res.status(404).json({
        error: 'Not found',
        path: req.originalUrl
      });
    });

    server = createServer(app);

    // WebSocket server setup for testing
    wss = new WebSocketServer({ server });
    wss.on('connection', (ws) => {
      ws.on('message', (data) => {
        try {
          const message = JSON.parse(data.toString());
          ws.send(JSON.stringify({ type: 'echo', data: message, timestamp: new Date().toISOString() }));
        } catch (error) {
          ws.send(JSON.stringify({ type: 'error', message: 'Invalid JSON format' }));
        }
      });
      ws.send(JSON.stringify({ type: 'welcome', message: 'Connected to GenZ Trading Bot Pro', timestamp: new Date().toISOString() }));
    });

    await new Promise<void>(resolve => server.listen(0, () => resolve()));
    const address = server.address();
    if (typeof address === 'string') {
        serverAddress = address;
    } else if (address) {
        serverAddress = `http://localhost:${address.port}`;
    }
  });

  afterAll(async () => {
    await new Promise<void>(resolve => {
        if (wss) {
            wss.close(() => resolve());
        } else {
            resolve();
        }
    });
    await new Promise<void>(resolve => {
        if (server) {
            server.close(() => resolve());
        } else {
            resolve();
        }
    });
  });

  describe('HTTP Server Tests', () => {
    it('should return health check with correct format', async () => {
      const response = await request(app).get('/health');
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('status', 'OK');
    });

    it('should handle CORS correctly', async () => {
      const response = await request(app).get('/health').set('Origin', 'http://localhost:3000');
      expect(response.headers['access-control-allow-origin']).toBe('http://localhost:3000');
    });

    it('should parse JSON correctly', async () => {
      const testData = { test: 'data' };
      const response = await request(app).post('/api/data').send(testData);
      expect(response.status).toBe(200);
      expect(response.body.received).toEqual(testData);
    });

    it('should handle large JSON payloads (under 10MB limit)', async () => {
      const largeData = { data: 'x'.repeat(1024 * 1024) };
      const response = await request(app).post('/api/data').send(largeData);
      expect(response.status).toBe(200);
    });

    it('should reject payloads exceeding 10MB limit', async () => {
      const oversizedData = { data: 'x'.repeat(11 * 1024 * 1024) };
      const response = await request(app).post('/api/data').send(oversizedData);
      expect(response.status).toBe(413);
    });

    it('should handle malformed JSON gracefully', async () => {
      const response = await request(app).post('/api/data').set('Content-Type', 'application/json').send('{ invalid json }');
      expect(response.status).toBe(400);
    });

    it('should handle server errors with proper error response', async () => {
      const response = await request(app).get('/api/error');
      expect(response.status).toBe(500);
      expect(response.body).toHaveProperty('error', 'Internal server error');
    });

    it('should return 404 for unknown routes', async () => {
      const response = await request(app).get('/non-existent-route');
      expect(response.status).toBe(404);
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty request body', async () => {
      const response = await request(app).post('/api/data').send({});
      expect(response.status).toBe(200);
      expect(response.body.received).toEqual({});
    });

    it('should handle null values in JSON', async () => {
      const testData = { nullValue: null };
      const response = await request(app).post('/api/data').send(testData);
      expect(response.status).toBe(200);
      expect(response.body.received).toEqual(testData);
    });

    it('should handle special characters and unicode', async () => {
      const testData = { text: '🚀 café' };
      const response = await request(app).post('/api/data').send(testData);
      expect(response.status).toBe(200);
      expect(response.body.received).toEqual(testData);
    });

    it('should handle arrays with mixed types', async () => {
      const testData = { mixed: [1, 'a', null] };
      const response = await request(app).post('/api/data').send(testData);
      expect(response.status).toBe(200);
      expect(response.body.received).toEqual(testData);
    });

    it('should handle deeply nested objects', async () => {
      const testData = { l1: { l2: { l3: 'deep' } } };
      const response = await request(app).post('/api/data').send(testData);
      expect(response.status).toBe(200);
      expect(response.body.received).toEqual(testData);
    });
  });

  describe('WebSocket Tests', () => {
    it('should establish WebSocket connection and send welcome message', async () => {
        await new Promise((resolve, reject) => {
            const ws = new WebSocket(serverAddress.replace('http', 'ws'));
            ws.on('message', (data) => {
                const message = JSON.parse(data.toString());
                if (message.type === 'welcome') {
                    expect(message.message).toBe('Connected to GenZ Trading Bot Pro');
                    ws.close();
                    resolve(true);
                }
            });
            ws.on('error', reject);
        });
    });

    it('should echo back valid JSON messages', async () => {
        await new Promise((resolve, reject) => {
            const ws = new WebSocket(serverAddress.replace('http', 'ws'));
            const testMessage = { action: 'test' };
            ws.on('open', () => ws.send(JSON.stringify(testMessage)));
            ws.on('message', (data) => {
                const message = JSON.parse(data.toString());
                if (message.type === 'echo') {
                    expect(message.data).toEqual(testMessage);
                    ws.close();
                    resolve(true);
                }
            });
            ws.on('error', reject);
        });
    });

    it('should handle invalid JSON messages gracefully', async () => {
        await new Promise((resolve, reject) => {
            const ws = new WebSocket(serverAddress.replace('http', 'ws'));
            ws.on('open', () => ws.send('{ invalid json }'));
            ws.on('message', (data) => {
                const message = JSON.parse(data.toString());
                if (message.type === 'error') {
                    expect(message.message).toBe('Invalid JSON format');
                    ws.close();
                    resolve(true);
                }
            });
            ws.on('error', reject);
        });
    });
  });
});