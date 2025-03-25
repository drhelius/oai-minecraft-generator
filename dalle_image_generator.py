import io
import uuid
import requests
import os
from openai_utils import OpenAIClient
from blob_storage_client import BlobStorageClient
from image_frame_processor import ImageFrameProcessor

class DalleImageGenerator:
    def __init__(self, container_name="minecraft"):
        self.openai_client = OpenAIClient(model_id="dalle")
        self.blob_client = BlobStorageClient(container_name)
        self.frame_processor = ImageFrameProcessor()
    
    def generate_minecraft_image(self, description, add_frame=True, frame_path="frames/frame1.png"):
        """Generate a Minecraft style image from a text description."""
        client = self.openai_client.get_client()
        deployment_name = self.openai_client.deployment_name
        
        # Enhanced prompt for Minecraft character generation
        enhanced_prompt = f"""
        A full-body Minecraft character depicting a friendly-looking {description}. The character stands in a vibrant Minecraft environment surrounded by lush pixelated grass blocks and stylized pixelated trees under a clear blue sky. The character must have all the classic Minecraft characteristics: Blocky, pixelated appearance with clear cube structure. Wide-angle view capturing the entire figure clearly, simulating a Minecraft screenshot. """
        
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
        
        # Apply frame if requested
        if add_frame and os.path.exists(frame_path):
            image_bytes = self.frame_processor.add_frame(image_bytes, frame_path)
        
        # Generate a unique filename for blob storage
        filename = f"minecraft_{uuid.uuid4().hex}.png"
        
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
