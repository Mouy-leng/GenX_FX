import pytest
import asyncio
from fastapi.testclient import TestClient
import os

# Set test environment variables
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test"
os.environ["MONGODB_URL"] = "mongodb://localhost:27017/test"
os.environ["REDIS_URL"] = "redis://localhost:6379"

from api.main import app

client = TestClient(app)

class TestEdgeCases:
    """Comprehensive edge case testing for the GenX FX API"""

    def test_health_endpoint_structure(self):
        """Test health endpoint returns correct structure"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "status" in data
        assert "timestamp" in data
        assert "database" in data

        # Validate timestamp format
        from datetime import datetime
        try:
            datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
        except ValueError:
            pytest.fail("Invalid timestamp format")

    def test_root_endpoint_completeness(self):
        """Test root endpoint has all required information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()

        required_fields = ["message", "version", "status", "github", "repository"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        assert data["status"] == "running"

    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        response = client.options("/")
        # The test client might not fully simulate CORS, but we can check basic structure
        assert response.status_code in [200, 405]  # OPTIONS might not be implemented

    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import threading
        import time

        results = []
        def make_request():
            response = client.get("/health")
            results.append(response.status_code)

        # Create multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 10

class TestPerformanceEdgeCases:
    """Test performance-related edge cases"""

    def test_response_time_reasonable(self):
        """Test that responses come back in reasonable time"""
        import time

        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()

        response_time = end_time - start_time
        assert response_time < 5.0, f"Health check took too long: {response_time}s"
        assert response.status_code == 200

class TestErrorHandling:
    """Test comprehensive error handling"""

    def test_undefined_endpoints(self):
        """Test handling of undefined endpoints"""
        undefined_endpoints = [
            "/api/v1/nonexistent",
            "/api/v1/admin/secret",
            "/api/v2/predictions/predict",  # Wrong version
            "/api/v1/predictions/delete_all",  # Dangerous endpoint
        ]

        for endpoint in undefined_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 404

            # Should return structured error
            if response.headers.get("content-type", "").startswith("application/json"):
                error_data = response.json()
                assert "detail" in error_data

    def test_method_not_allowed(self):
        """Test handling of wrong HTTP methods"""
        # Try wrong methods on existing endpoints
        test_cases = [
            ("DELETE", "/"),
            ("PUT", "/health"),
            ("POST", "/trading-pairs"),
        ]

        for method, endpoint in test_cases:
            response = client.request(method, endpoint)
            assert response.status_code in [405, 404]  # Method Not Allowed or Not Found

if __name__ == "__main__":
    pytest.main([__file__, "-v"])