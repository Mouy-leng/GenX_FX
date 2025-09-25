# Local Development Setup

This document provides instructions for setting up a local development environment for the GenX FX Trading Platform.

## Prerequisites

*   Python 3.13 or higher
*   Docker and Docker Compose
*   An AWS account with the AWS CLI configured (only if you want to fetch secrets from AWS Secrets Manager)

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Mouy-leng/GenX_FX.git
    cd GenX_FX
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**

    *   Copy the `.env.example` file to a new file named `.env`:

        ```bash
        cp .env.example .env
        ```

    *   Open the `.env` file and fill in your credentials for the services you want to use. You do not need to fill in all of them, only the ones you need for the features you are working on.

5.  **Run the application:**

    ```bash
    docker-compose up --build
    ```

    This will start the application and all the required services. The API will be available at `http://localhost:8080`.

## Running Tests

To run the tests, you will need to install the test dependencies:

```bash
pip install pytest
```

Then, you can run the tests using the following command:

```bash
python3 run_tests.py
```

## AWS Secrets Manager (Optional)

If you want to fetch secrets from AWS Secrets Manager instead of using a `.env` file, you will need to:

1.  **Configure your AWS credentials:**

    Make sure your AWS CLI is configured with the necessary credentials to access your AWS account.

2.  **Set the `AWS_REGION` environment variable:**

    If your secrets are not in the `us-east-1` region, you will need to set the `AWS_REGION` environment variable to the correct region.

3.  **Unset the environment variables in your `.env` file:**

    If an environment variable is set in your `.env` file, the application will use that value instead of fetching the secret from AWS Secrets Manager. To force the application to fetch a secret from AWS Secrets Manager, you will need to remove the corresponding environment variable from your `.env` file.