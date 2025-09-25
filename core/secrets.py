import boto3
import json
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

class SecretManager:
    """
    A class to manage fetching secrets from environment variables or AWS Secrets Manager.
    """
    _instance = None
    _secrets_cache = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecretManager, cls).__new__(cls)
            cls._secrets_cache = {}
            if os.environ.get("APP_ENV") != "production":
                load_dotenv()
        return cls._instance

    def get_secret(self, secret_name, is_json=False):
        """
        Retrieves a secret from environment variables first, then from AWS Secrets Manager
        if APP_ENV is set to production.
        Caches secrets in memory to avoid repeated API calls.
        """
        # Check environment variables first
        secret_value = os.environ.get(secret_name)
        if secret_value:
            return json.loads(secret_value) if is_json else secret_value

        # If not in env, check cache
        if secret_name in self._secrets_cache:
            return self._secrets_cache[secret_name]

        # If in production, fetch from AWS Secrets Manager
        if os.environ.get("APP_ENV") == "production":
            region_name = os.environ.get("AWS_REGION", "us-east-1")
            session = boto3.session.Session()
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name
            )

            try:
                # Use a consistent naming convention for secrets in AWS Secrets Manager
                aws_secret_name = f"/genx-fx/production/{secret_name.lower()}"
                get_secret_value_response = client.get_secret_value(
                    SecretId=aws_secret_name
                )
            except ClientError as e:
                # For a list of exceptions thrown, see
                # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
                raise e

            # Decrypts secret using the associated KMS key.
            secret = get_secret_value_response['SecretString']

            if is_json:
                secret = json.loads(secret)

            self._secrets_cache[secret_name] = secret
            return secret

        return None

# Singleton instance
secrets_manager = SecretManager()