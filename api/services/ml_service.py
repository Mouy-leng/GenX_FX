import asyncio

class MLService:
    """
    A dummy ML service for testing purposes.
    This class simulates the interface of a real machine learning service.
    """
    async def initialize(self):
        """Simulates the initialization of the ML service."""
        print("ML Service Initialized (dummy).")
        await asyncio.sleep(0.01)

    async def predict(self, symbol: str, data: dict):
        """Simulates making a prediction."""
        print(f"Predicting for {symbol} (dummy).")
        await asyncio.sleep(0.01)
        return {"signal": "hold", "confidence": 0.5}

    async def health_check(self):
        """Simulates a health check for the ML service."""
        return "healthy"

    async def shutdown(self):
        """Simulates the shutdown of the ML service."""
        print("ML Service Shutdown (dummy).")
        await asyncio.sleep(0.01)