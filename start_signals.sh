#!/bin/bash
mkdir -p logs
nohup python3 signal_generator.py >> logs/signal_generator.log 2>&1 &
echo $! > logs/signal_generator.pid
echo "[STARTED] Signal generator running with PID $(cat logs/signal_generator.pid)"
