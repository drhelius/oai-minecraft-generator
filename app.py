import streamlit as st
import os
from dalle_image_generator import DalleImageGenerator
from qr_code_generator import generate_qr_code
from PIL import Image
import pyperclip

st.set_page_config(
    page_title="Minecraft-style Character Generator",
    page_icon="⛏️",
    layout="centered"
)

def main():
    st.title("⛏️ Minecraft-style Character Generator")
    st.write("Enter a description and generate a Minecraft-style character!")
    
    # Initialize the image generator
    image_generator = DalleImageGenerator()
    
    # Store the last used description and biome in session state
    if 'last_description' not in st.session_state:
        st.session_state.last_description = ""
    
    if 'last_biome' not in st.session_state:
        st.session_state.last_biome = "Forest"
    
    # Track if we should regenerate the image
    if 'regenerate' not in st.session_state:
        st.session_state.regenerate = False
    
    # List of Minecraft biomes
    biomes = [
        "Beach", "Desert", "Forest", "Jungle", 
        "Plains", "River", "Savanna", "Snowy Slopes", "Swamp",
        "Nether", "End"
    ]
    
    # Add biome selection dropdown
    # selected_biome = st.selectbox(
    #     "Select background biome:",
    #     biomes,
    #     index=biomes.index(st.session_state.last_biome) if st.session_state.last_biome in biomes else 5  # Default to Plains
    # )
    selected_biome = "Forest"
    
    # Handle regeneration from previous run
    if st.session_state.regenerate and st.session_state.last_description:
        st.session_state.regenerate = False
        generate_minecraft_image(st.session_state.last_description, selected_biome, image_generator)
    
    # Use chat_input instead of form with text_area and button
    description = st.chat_input(
        placeholder="Example: A zombie warrior with diamond armor and enchanted sword",
    )
    
    # Process the input when user submits
    if description:
        # Copy the description to clipboard
        try:
            pyperclip.copy(description)
        except Exception as e:
            print(f"Could not copy to clipboard: {str(e)}")
            
        # Store the description and biome in session state
        st.session_state.last_description = description
        st.session_state.last_biome = selected_biome
        
        generate_minecraft_image(description, selected_biome, image_generator)

    # Generate Again button - only show if there's a previous description
    if st.session_state.last_description:
        st.text(" ")
        st.text(" ")
        if st.button("🔄 Generate Again with Same Prompt", use_container_width=True):
            # Set flag to regenerate and trigger a rerun
            st.session_state.regenerate = True
            st.rerun()

def generate_minecraft_image(description, biome, image_generator):
    with st.spinner(f"Generating your character..."):
    #with st.spinner(f"Generating your character in a {biome} biome..."):
        try:
            # Generate the image with frame included
            result = image_generator.generate_minecraft_image(description, biome)
            
            # Create two columns for displaying images side by side
            col1, col2 = st.columns(2)
            
            with col1:
                # Display image directly from bytes without caption
                st.image(result["image_bytes"], use_container_width=True)
                st.markdown(f"<div style='text-align: center;'>Generated Character</div>", unsafe_allow_html=True)
            
            # Generate QR code for the blob URL
            qr_bytes = generate_qr_code(result["blob_url"])
            
            with col2:
                # Display QR code directly from bytes without caption
                st.image(qr_bytes, use_container_width=True)
                st.markdown(f"<div style='text-align: center;'>Scan QR Code or use this <a href='{result['blob_url']}' target='_blank'>direct link</a></div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error generating image: {str(e)}")

if __name__ == "__main__":
    main()
