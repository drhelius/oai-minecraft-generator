import io
import uuid
import requests
from openai_utils import OpenAIClient
from blob_storage_client import BlobStorageClient

class DalleImageGenerator:
    def __init__(self, container_name="images"):
        self.openai_client = OpenAIClient(model_id="dalle")
        self.blob_client = BlobStorageClient(container_name)
    
    def generate_funko_image(self, description):
        """Generate a Funko-Pop style image from a text description."""
        client = self.openai_client.get_client()
        deployment_name = self.openai_client.deployment_name
        
        # Enhanced prompt for more accurate Funko Pop figurines
        enhanced_prompt = f"""
Create a photorealistic image of an official Funko Pop vinyl figure based on this description: {description}.

The figure must have all the classic Funko Pop characteristics:
- Square-shaped head that's disproportionately large compared to the body (about 1/3 of the total height)
- Small, simplified body with basic pose
- Solid black circular eyes with no pupils (the defining Funko feature)
- No mouth or a very simple mouth
- Minimal facial details, just the essential recognizable features
- Small nose or no nose at all
- Simplified hairstyle with clean, solid shapes
- Arms at the sides or in a signature pose
- The figure should be standing on a square black base

The figure should be displayed in a professional product photography style:
- Clean studio lighting with soft shadows
- Displayed inside the official Funko Pop clear plastic box with the black "POP!" logo in the top corner
- Crisp, clear focus on the figure
- Slight 3/4 angle view showing front and side
- Clean background with slight gradient

The image should be indistinguishable from an official Funko Pop product photo found on online stores.
"""
        
        # Generate image using DALL-E
        response = client.images.generate(
            model=deployment_name,
            prompt=enhanced_prompt,
            n=1,
            size="1024x1024",
            response_format="url"
        )
        
        # Get the image URL from the response
        image_url = response.data[0].url
        
        # Download the image into memory
        image_response = requests.get(image_url)
        image_bytes = io.BytesIO(image_response.content)
        
        # Generate a unique filename for blob storage
        filename = f"funko_{uuid.uuid4().hex}.png"
        
        # Upload directly from memory to blob storage
        self.blob_client.upload_bytes(image_bytes, filename)
        
        # Get the blob URL
        blob_url = self.blob_client.get_blob_url(filename)
        
        # Reset the stream position to start for Streamlit to read
        image_bytes.seek(0)
        
        return {
            "image_bytes": image_bytes,
            "blob_url": blob_url,
            "filename": filename
        }
