#!/bin/bash
if [ -f logs/signal_generator.pid ]; then
    kill $(cat logs/signal_generator.pid)
    rm logs/signal_generator.pid
    echo "[STOPPED] Signal generator stopped."
else
    echo "No running signal generator found."
fi
