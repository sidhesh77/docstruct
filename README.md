# DocStruct — AI-Powered KYC Document Intelligence

A full-stack document intelligence platform that extracts, structures, and validates KYC data from PDFs using AI — built for enterprise automation workflows.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41-red)
![Gemini AI](https://img.shields.io/badge/Gemini-2.0_Flash-purple)
![Auth](https://img.shields.io/badge/Auth-bcrypt+SQLite-green)

---

## Features

- **Secure Authentication** — Register/login with bcrypt-hashed passwords (SQLite backend)
- **AI Extraction** — Google Gemini 2.0 Flash for intelligent field parsing
- **Demo Fallback** — Rule-based parser works without API key
- **Validation Engine** — PAN, phone, date, and address compliance checks
- **Dashboard** — Extraction history and activity tracking per user
- **Modern UI** — Custom dark theme, pipeline visualization, responsive layout
- **JSON Export** — One-click download of structured output

---

## Quick Start

```bash
cd docstruct
pip3 install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`

**Demo login:** `demo` / `demo123`

---

## Optional: Enable Gemini AI

```bash
cp .env.example .env
# Add your key from https://aistudio.google.com/apikey
```

---

## Architecture

```
Upload (PDF/TXT) → Text Extraction → AI/Demo Parser → Validation → JSON Export
                         ↑                                              ↓
                   pdfplumber                                    SQLite History
```

| Module | Purpose |
|--------|---------|
| `app.py` | Main UI, routing, pipeline orchestration |
| `auth.py` | User registration, login, extraction history |
| `extract_text.py` | PDF/TXT text extraction |
| `extract_json.py` | Gemini AI + demo parser |
| `validate_data.py` | Field validation rules |
| `ui_styles.py` | Custom CSS and UI components |

---

## Sample Output

```json
{
  "full_name": "Rahul Sharma",
  "date_of_birth": "1998-05-12",
  "pan_number": "ABCDE1234F",
  "aadhaar_last4": "4821",
  "address": "House No. 42, Sector 14, Gurugram, Haryana - 122001",
  "phone": "+91 9876543210",
  "document_type": "KYC"
}
```

---

## Resume Bullet

> Built **DocStruct**, an AI-powered document intelligence platform that automates KYC data extraction from PDFs into validated JSON — featuring secure authentication, Gemini AI integration, extraction history dashboard, and a full compliance validation pipeline.

---

## Tech Stack

Python · Streamlit · Google Gemini API · pdfplumber · SQLite · bcrypt · python-dotenv