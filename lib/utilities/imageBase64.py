from PIL import Image
from base64 import b64encode
import io

def image_to_base64(image_path: str) -> str:
    """Convert a Pillow Image into a base64 string."""
    
    # Open the image file
    with Image.open(image_path) as image:
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
    return b64encode(buf.getvalue()).decode()

