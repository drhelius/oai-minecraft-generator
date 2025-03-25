import base64
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import os
from models_config import get_env_variable_keys
import logging

class WebcamAnalyzer:
    def __init__(self, model_id="mistral"):
        """Initialize the webcam analyzer with the LLM model."""
        self.model_id = model_id
        env_keys = get_env_variable_keys(self.model_id)
        
        self.endpoint = os.getenv(env_keys["endpoint"])
        self.api_key = os.getenv(env_keys["api_key"])
        self.deployment_name = os.getenv(env_keys["deployment_name"])
        
        if not all([self.endpoint, self.api_key, self.deployment_name]):
            missing = [key for key, val in env_keys.items() if not os.getenv(val)]
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def analyze_face(self, image_bytes):
        """
        Analyze the facial features from a webcam image using Azure AI Inference API.
        
        Args:
            image_bytes: The webcam image as bytes
            
        Returns:
            A string description of the facial features
        """
        self.logger.info(f"Creating client with endpoint: {self.endpoint}")
        # Create client with endpoint and key
        client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )
        
        # Convert image to base64 for inclusion in the prompt
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        self.logger.info("Image converted to base64")
        
        # Prepare message for the model
        messages = [
            {
                "role": "system", 
                "content": "You are an AI assistant that analyzes facial features. Look at the provided image and list the key facial features that would be important for a Minecraft character. Return ONLY a comma-separated list of features without additional explanation. For example: 'blonde hair, blue eyes, beard, glasses, smiling'."
            },
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text", 
                        "text": "Analyze this facial image and provide a comma-separated list of key features"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            }
        ]
        
        self.logger.info(f"Calling model with deployment name: {self.deployment_name}")
        
        try:
            # Call the model
            response = client.complete(
                model=self.deployment_name,
                messages=messages,
                temperature=0.7,
                max_tokens=200,
                top_p=1.0
            )
            
            self.logger.info(f"Received response from model: {response}")
            
            # Return the description
            content = response.choices[0].message.content.strip()
            self.logger.info(f"Extracted content: {content}")
            return content
        except Exception as e:
            self.logger.error(f"Error calling Azure AI model: {str(e)}")
            raise Exception(f"Error analyzing image: {str(e)}")
