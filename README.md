# Resume Scanner App 🚀

This is a Streamlit application that analyzes resumes and matches them against job descriptions using Google's Gemini AI.

## Features
- Upload your Resume (PDF)
- Enter a Job Description
- Get a professional review about your Resume
- Get a match percentage and missing keywords

## Tech Stack
- Python
- Streamlit
- Gemini 1.5 Flash (Google Generative AI)
- pdf2image
- PIL (Pillow)

## Setup Instructions (Local)
1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies:

```bash
pip install -r requirements.txt

## How to run locally:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up `.env` file with your Google API Key
4. Run: `streamlit run app.py`

## Environment Variables

- `GOOGLE_API_KEY`: Your Google Gemini API key.
