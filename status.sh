#!/bin/bash
if [ -f logs/signal_generator.pid ]; then
    PID=$(cat logs/signal_generator.pid)
    if ps -p $PID > /dev/null; then
        echo "[RUNNING] Signal generator is active with PID $PID."
    else
        echo "[ERROR] PID file exists but process is not running."
    fi
else
    echo "[STOPPED] No signal generator running."
fi
