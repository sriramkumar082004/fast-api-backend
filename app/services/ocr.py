import re
from typing import Dict, Any
from PIL import Image
import pytesseract
import io

# Ensure Tesseract is in your path or configure it here
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_aadhaar_info(image_bytes: bytes) -> Dict[str, Any]:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)

        # Basic extraction logic (heuristics)
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Regex patterns
        dob_pattern = r"\d{2}/\d{2}/\d{4}"
        aadhaar_pattern = r"\d{4}\s\d{4}\s\d{4}"

        extracted_data = {
            "name": None,
            "dob": None,
            "aadhaar_last_4": None,
            "raw_text_snippet": text[:200],
        }

        # Extract DOB
        dob_match = re.search(dob_pattern, text)
        if dob_match:
            extracted_data["dob"] = dob_match.group(0)

        # Extract Aadhaar
        aadhaar_match = re.search(aadhaar_pattern, text)
        if aadhaar_match:
            full_aadhaar = aadhaar_match.group(0)
            extracted_data["aadhaar_last_4"] = full_aadhaar[-4:]

        # Extract Name - Heuristic: Line before DOB or near top
        # This is fragile and depends on card layout
        for i, line in enumerate(lines):
            if "Year of Birth" in line or "DOB" in line:
                if i > 0:
                    extracted_data["name"] = lines[i - 1]
                break

        # Fallback for name if not found strictly
        if not extracted_data["name"] and len(lines) > 2:
            extracted_data["name"] = lines[1]  # Guessing second line often name

        return extracted_data
    except Exception as e:
        return {"error": str(e)}
