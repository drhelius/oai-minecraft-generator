import base64
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import os
from models_config import get_env_variable_keys

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
        
    def analyze_face(self, image_bytes):
        """
        Analyze the facial features from a webcam image using Azure AI Inference API.
        """
        # Create client with endpoint and key
        client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )
        
        # Convert image to base64 for inclusion in the prompt
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Prepare message for the model
        messages = [
            {
                "role": "system", 
                "content": """Analyze the provided photo of a person and extract:

- Gender (e.g., boy, girl, man, woman, etc.)
- Approximate age
- Facial features (e.g., eye color, shape of eyes, nose, mouth, etc.)
- Hair (e.g., color, length, style, etc.)
- Skin tone
- Any distinguishing marks (e.g., scars, birthmarks, tattoos, etc.)
- Accessories (e.g., glasses, earrings, etc.)

Your answer must be ONLY a single and concise comma separated list of features without additional explanation.

If you don't find some of the features omit them in the answer: Don't say something like 'no visible marks'."""
            },
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text", 
                        "text": "Analyze this facial image"
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
        
        try:
            # Call the model
            response = client.complete(
                model=self.deployment_name,
                messages=messages,
                temperature=0.7,
                max_tokens=200,
                top_p=1.0
            )
            
            # Return the description
            content = response.choices[0].message.content.strip()
            return content
        except Exception as e:
            print(f"Error calling Azure AI model: {str(e)}")
            raise Exception(f"Error analyzing image: {str(e)}")
