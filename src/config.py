import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Folders
INPUT_FOLDER = "input_documents"
REPORT_FOLDER = "output_reports"
OUTPUT_FOLDER = "output_images"
EXTRACTION_OUTPUT_FOLDER = "extracted_text_documents"