import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import json
from botocore.exceptions import ClientError

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def mock_aws_secrets():
    """Mocks the boto3 client for Secrets Manager."""

    mock_secrets = {
        "/genx-fx/production/gemini_api_key": "test_gemini_api_key",
        "/genx-fx/production/newsapi_org_key": "test_news_api_key",
        "/genx-fx/production/bybit_api_key": "test_bybit_api_key",
        "/genx-fx/production/bybit_api_secret": "test_bybit_api_secret",
        "/genx-fx/production/reddit_client_id": "test_reddit_client_id",
        "/genx-fx/production/reddit_client_secret": "test_reddit_client_secret",
        "/genx-fx/production/telegram_bot_token": "test_telegram_bot_token",
    }

    def mock_get_secret_value(SecretId):
        secret_string = mock_secrets.get(SecretId)
        if secret_string:
            return {
                'SecretString': secret_string,
                'ARN': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:test-secret-123456',
                'Name': SecretId,
                'VersionId': '12345678-1234-1234-1234-123456789012',
                'VersionStages': ['AWSCURRENT'],
                'CreatedDate': '2023-01-01T00:00:00.000Z'
            }
        else:
            # Simulate SecretNotFoundException
            raise ClientError({'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secrets Manager can''t find the specified secret.'}}, 'GetSecretValue')

    with patch('core.secrets.boto3.client') as mock_boto_client:
        mock_sm_client = MagicMock()
        mock_sm_client.get_secret_value.side_effect = mock_get_secret_value
        mock_boto_client.return_value = mock_sm_client
        yield