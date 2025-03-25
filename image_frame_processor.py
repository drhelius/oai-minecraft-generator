import io
from PIL import Image

class ImageFrameProcessor:
    def __init__(self, frames_directory="frames"):
        self.frames_directory = frames_directory
    
    def add_frame(self, image_bytes, frame_path):
        """
        Add a frame to an image.
        
        Args:
            image_bytes (io.BytesIO): The image as bytes
            frame_path (str): Path to the frame image
            
        Returns:
            io.BytesIO: The processed image with frame added
        """
        # Open the image bytes with PIL
        base_image = Image.open(image_bytes).convert("RGBA")
        
        # Open the frame
        frame = Image.open(frame_path).convert("RGBA")
        
        # Ensure the frame is the right size (same as base image)
        if frame.size != base_image.size:
            frame = frame.resize(base_image.size)
        
        # Composite the images (place frame on top of the base image)
        composite = Image.alpha_composite(base_image, frame)
        
        # Convert back to RGB if needed
        final_image = composite.convert("RGB")
        
        # Save the result to bytes
        result_bytes = io.BytesIO()
        final_image.save(result_bytes, format="PNG")
        result_bytes.seek(0)  # Reset the pointer to the beginning
        
        return result_bytes
