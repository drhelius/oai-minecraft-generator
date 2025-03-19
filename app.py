import streamlit as st
import os
from dalle_image_generator import DalleImageGenerator
from qr_code_generator import generate_qr_code
from PIL import Image

st.set_page_config(
    page_title="Funko Pop Generator",
    page_icon="🎭",
    layout="centered"
)

def main():
    st.title("🎭 Funko Pop Image Generator")
    st.write("Enter a description of a person and generate a Funko Pop style image!")
    
    # Initialize the image generator
    image_generator = DalleImageGenerator()
    
    # Use chat_input instead of form with text_area and button
    description = st.chat_input(
        placeholder="Example: Albert Einstein with crazy hair and a lab coat",
    )
    
    # Process the input when user submits
    if description:
        with st.spinner("Generating your Funko Pop image..."):
            try:
                # Generate the image
                result = image_generator.generate_funko_image(description)
                
                # Display the generated image and QR code side by side
                st.success("Image generated successfully!")
                
                # Create two columns for displaying images side by side
                col1, col2 = st.columns(2)
                
                with col1:
                    # Display image directly from bytes
                    st.image(result["image_bytes"], caption="Generated Funko Pop Image", use_container_width=True)
                
                # Generate QR code for the blob URL
                qr_bytes = generate_qr_code(result["blob_url"])
                
                with col2:
                    # Display QR code directly from bytes
                    st.image(qr_bytes, caption="Scan QR Code to Download", use_container_width=True)
                
                # Display the blob URL below the images
                st.markdown(f"Or use this [direct link]({result['blob_url']})")
                
            except Exception as e:
                st.error(f"Error generating image: {str(e)}")

if __name__ == "__main__":
    main()
