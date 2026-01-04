from typing import Any

from PIL import Image, ImageDraw, ImageFont

# Create a placeholder background image
img = Image.new("RGB", (700, 500), color=(70, 130, 180))
d = ImageDraw.Draw(img)
try:
    # PIL's ImageFont.truetype can return types that mypy has trouble inferring
    # Use a broad Any annotation to satisfy type checker while keeping runtime behavior
    font: Any = ImageFont.truetype("arial.ttf", 72)  # type: ignore[assignment]
except Exception:
    font = ImageFont.load_default()
text = "IODEX"
bbox = d.textbbox((0, 0), text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
d.text(((700 - text_w) / 2, (500 - text_h) / 2), text, fill=(255, 255, 255), font=font)
img.save("photo1.jpg", "JPEG")

# Create an ICO version
sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
img.save("app.ico", sizes=sizes)
print("Generated photo1.jpg and app.ico")
