"""
Step 3: Check if the extracted data looks correct.

Simple rules — no fancy libraries needed.
"""

import re


def validate_pan(pan: str) -> bool:
    """
    Indian PAN format: 5 letters + 4 digits + 1 letter
    Example: ABCDE1234F
    """
    if not pan:
        return False
    pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"
    return bool(re.match(pattern, pan.strip().upper()))


def validate_phone(phone: str) -> bool:
    """Accept 10-digit Indian numbers (with or without +91)."""
    if not phone:
        return False
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    return len(digits) == 10


def validate_date(date_str: str) -> bool:
    """Accept dates like 1998-05-12 or 12/05/1998."""
    if not date_str:
        return False
    patterns = [
        r"^\d{4}-\d{2}-\d{2}$",
        r"^\d{2}/\d{2}/\d{4}$",
        r"^\d{2}-\d{2}-\d{4}$",
    ]
    return any(re.match(p, date_str.strip()) for p in patterns)


def check_all_fields(data: dict) -> dict:
    """
    Run checks on each field and return a simple report.

    Returns a dict like:
    {
        "full_name": {"value": "Rahul", "ok": True, "message": "OK"},
        "pan_number": {"value": "BAD", "ok": False, "message": "Invalid PAN format"},
        ...
    }
    """
    fields = {
        "full_name": lambda v: (bool(v and len(v.strip()) > 1), "Name is missing"),
        "date_of_birth": lambda v: (validate_date(v), "Invalid date format"),
        "pan_number": lambda v: (validate_pan(v), "Invalid PAN format (e.g. ABCDE1234F)"),
        "phone": lambda v: (validate_phone(v), "Invalid phone (need 10 digits)"),
        "address": lambda v: (bool(v and len(v.strip()) > 5), "Address is too short"),
    }

    report = {}
    for field_name, check_fn in fields.items():
        value = data.get(field_name, "") or ""
        is_ok, error_msg = check_fn(value)
        report[field_name] = {
            "value": value,
            "ok": is_ok,
            "message": "OK" if is_ok else error_msg,
        }

    return report