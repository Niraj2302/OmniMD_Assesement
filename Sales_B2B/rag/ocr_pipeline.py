from pathlib import Path
from PIL import Image
import pytesseract

async def retrieve_ocr(prospect_id: str) -> list[str]:
    path = Path(f"knowledge/ocr/card_{prospect_id}.png")
    if not path.exists():
        return []
    try:
        image = Image.open(path)
        text = pytesseract.image_to_string(image)
        return [f"OCR Content: {text.strip()}"]
    except Exception:
        return []