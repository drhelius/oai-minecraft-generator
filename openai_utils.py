import os
from models_config import get_env_variable_keys
from openai import AzureOpenAI

class OpenAIClient:
    def __init__(self, model_id="gpt4o_1"):
        self.model_id = model_id
        self.deployment_name = ""

    def get_client(self):
        env_keys = get_env_variable_keys(self.model_id)

        endpoint = os.getenv(env_keys["endpoint"])
        api_key = os.getenv(env_keys["api_key"])
        api_version = os.getenv(env_keys["api_version"])
        self.deployment_name = os.getenv(env_keys["deployment_name"])
        api_type = os.getenv(env_keys["api_type"])

        if not all([endpoint, api_key, api_version, self.deployment_name, api_type]):
            missing = [key for key, val in env_keys.items() if not os.getenv(val)]
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
            max_retries=3,
            timeout=60  # Increased timeout for image generation
        )

        return client
