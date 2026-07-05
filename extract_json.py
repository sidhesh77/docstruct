"""
Step 2: Turn raw text into structured JSON.

Uses Google Gemini AI when you have an API key.
Falls back to a demo parser when you don't (so you can still test the app).
"""

import json
import os
import re
from typing import Tuple

from dotenv import load_dotenv

load_dotenv()

# These are the fields we always want from a KYC document
KYC_FIELDS = [
    "full_name",
    "date_of_birth",
    "pan_number",
    "aadhaar_last4",
    "address",
    "phone",
    "document_type",
]


def _build_prompt(raw_text: str) -> str:
    """Instructions we send to Gemini."""
    return f"""
You are a document data extraction assistant for KYC forms.

Read the text below and extract these fields:
- full_name
- date_of_birth (use YYYY-MM-DD if possible)
- pan_number
- aadhaar_last4 (last 4 digits only)
- address
- phone
- document_type (usually "KYC")

Rules:
- Return ONLY valid JSON, no markdown, no explanation.
- If a field is missing, use an empty string "".
- Do not invent data that is not in the text.

Document text:
---
{raw_text}
---
"""


def extract_with_gemini(raw_text: str) -> dict:
    """
    Call Gemini API to extract JSON from text.

    Raises an error if API key is missing or API fails.
    """
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_api_key_here":
        raise ValueError(
            "No Gemini API key found. Copy .env.example to .env and add your key."
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    response = model.generate_content(_build_prompt(raw_text))
    response_text = response.text.strip()

    # Sometimes AI wraps JSON in ```json ... ``` — remove that
    response_text = re.sub(r"^```json\s*", "", response_text)
    response_text = re.sub(r"^```\s*", "", response_text)
    response_text = re.sub(r"\s*```$", "", response_text)

    data = json.loads(response_text)

    # Keep only the fields we care about
    return {field: str(data.get(field, "") or "") for field in KYC_FIELDS}


def extract_with_demo_parser(raw_text: str) -> dict:
    """
    Simple rule-based extractor — no AI needed.

    Good for learning and testing. Looks for patterns like:
    Name: Rahul Sharma
    PAN: ABCDE1234F
    """
    text = raw_text.replace("\n", " ")

    def find_after_label(label: str) -> str:
        pattern = rf"{label}\s*[:\-]?\s*([^\n|]+)"
        match = re.search(pattern, raw_text, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    pan_match = re.search(r"\b[A-Z]{5}\d{4}[A-Z]\b", text.upper())
    phone_match = re.search(r"(?:\+91[\s-]?)?[6-9]\d{9}", text)
    date_match = re.search(r"\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}", text)
    aadhaar_match = re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\s?(\d{4})\b", text)

    return {
        "full_name": find_after_label("name") or find_after_label("full name"),
        "date_of_birth": date_match.group(0) if date_match else find_after_label("dob"),
        "pan_number": pan_match.group(0) if pan_match else find_after_label("pan"),
        "aadhaar_last4": aadhaar_match.group(1) if aadhaar_match else "",
        "address": find_after_label("address"),
        "phone": phone_match.group(0) if phone_match else find_after_label("phone"),
        "document_type": "KYC",
    }


def extract_kyc_data(raw_text: str, use_ai: bool = True) -> Tuple[dict, str]:
    """
    Main function used by the app.

    Returns:
        (extracted_data, mode_used)
        mode_used is either "gemini" or "demo"
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("No text found in the document. Try a different file.")

    if use_ai:
        try:
            return extract_with_gemini(raw_text), "gemini"
        except Exception:
            # If AI fails, fall back so the app still works
            return extract_with_demo_parser(raw_text), "demo"

    return extract_with_demo_parser(raw_text), "demo"