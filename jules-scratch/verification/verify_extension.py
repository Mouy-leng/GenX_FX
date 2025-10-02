import os
import re
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        extension_path = Path(__file__).parent.parent.parent.joinpath("chrome-extension")
        user_data_dir = "/tmp/test-user-data-dir"

        # Launch a persistent browser context with the extension loaded
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=True,
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ],
        )

        # Wait for the service worker to be available
        try:
            service_worker = context.wait_for_event("serviceworker")
            print("Service worker found.")
        except Exception as e:
            print(f"Could not find service worker: {e}")
            context.close()
            return

        # Get the extension ID from the service worker's URL
        extension_id_match = re.search(r"extension://([^/]+)", service_worker.url)
        if not extension_id_match:
            print("Could not determine extension ID.")
            context.close()
            return
        extension_id = extension_id_match.group(1)
        print(f"Extension ID: {extension_id}")

        # Open the extension's popup page
        popup_page = context.new_page()
        popup_url = f"extension://{extension_id}/popup.html"
        print(f"Navigating to popup: {popup_url}")
        popup_page.goto(popup_url)

        # Wait for the WebSocket connection to be established
        print("Waiting for WebSocket connection...")
        expect(popup_page.locator("#signals-container")).to_contain_text("Connected. Waiting for signals...", timeout=10000)
        print("WebSocket connected.")

        # Give a moment for the server to be fully ready
        time.sleep(1)

        # Use Playwright's API request context to trigger a signal broadcast
        print("Broadcasting test signal via API...")
        api_request_context = p.request.new_context()
        test_signal = {
            "signal": "BUY",
            "symbol": "EURUSD",
            "entryPrice": 1.1000,
            "stopLoss": 1.0950,
            "targetPrice": 1.1050,
            "confidence": 0.85,
            "reasoning": "Test signal from verification script"
        }
        response = api_request_context.post(
            "http://localhost:5000/api/mt45/broadcast-signal",
            data={"signal": test_signal}
        )

        if not response.ok:
            print(f"API call failed: {response.status} {response.status_text}")
            print(f"Response body: {response.text()}")
            context.close()
            return

        print("API call successful.")

        # Verify that the signal is displayed in the popup
        print("Verifying signal in popup UI...")
        expect(popup_page.locator(".signal h2")).to_have_text("BUY EURUSD")
        expect(popup_page.locator(".signal ul")).to_contain_text("Entry Price: 1.1")
        print("Signal verified in UI.")

        # Take a screenshot for visual confirmation
        screenshot_path = "jules-scratch/verification/verification.png"
        popup_page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        # Clean up
        context.close()
        api_request_context.dispose()

if __name__ == "__main__":
    run_verification()