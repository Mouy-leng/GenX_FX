#!/usr/bin/env python3
import time
import csv
import datetime
from datetime import timezone
import os

OUTPUT_FILE = "dummy_signals.csv"

def generate_signal():
    now = datetime.datetime.now(timezone.utc)
    # Example dummy signal: alternate between BUY and SELL
    signal = "BUY" if now.minute % 2 == 0 else "SELL"

    return {
        "timestamp": now.isoformat(),
        "symbol": "XAUUSD",
        "signal": signal,
        "confidence": round(0.7, 2)  # fixed 70% confidence as placeholder
    }

def write_signal_to_csv(signal_data):
    file_exists = os.path.isfile(OUTPUT_FILE)
    with open(OUTPUT_FILE, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=signal_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(signal_data)

def main():
    print("[INFO] Signal generator started. Generating signals every 5 minutes...")
    while True:
        signal = generate_signal()
        write_signal_to_csv(signal)
        print(f"[{signal['timestamp']}] Generated signal: {signal['signal']}")
        time.sleep(300)  # wait 5 minutes

if __name__ == "__main__":
    main()