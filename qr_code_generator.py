import qrcode
import os
import uuid

def generate_qr_code(url, output_folder="qr_codes"):
    """Generate a QR code for the given URL."""
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Generate a unique filename
    filename = f"qr_{uuid.uuid4().hex}.png"
    output_path = os.path.join(output_folder, filename)
    
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    
    return output_path
