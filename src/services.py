import os
from pdf2image import convert_from_path
from PIL import Image
import google.generativeai as genai
from config import GEMINI_API_KEY, OUTPUT_FOLDER

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)


# 🔹 Convert PDF to Images
def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    """Convert a PDF file to images."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    images = convert_from_path(pdf_path, dpi=dpi)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i+1}.jpg')
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)
    return image_paths


# 🔹 Extract Text from Images Using Gemini AI
def ocr_with_gemini(image_paths, instruction):
    """Extract text from images using Gemini."""
    images = [Image.open(path) for path in image_paths]
    prompt = f"""
    {instruction}
    Extract only the text. Preserve tables using Markdown.
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt, *images])
    return response.text if response and hasattr(response, "text") else "OCR extraction failed."


# 🔹 Compute Pitch Score
def compute_pitch_score(data):
    # Define weights for each criterion (total should sum to 1 or 100%)
    weights = {
        "problem_statement": 0.15,  # 15%
        "solution": 0.20,  # 20%
        "business_model": 0.10,  # 10%
        "traction": 0.10,  # 10%
        "financials": 0.10,  # 10%
        "pitch_quality": 0.10,  # 10%
        "market_analysis": 0.15,  # 15%
        "team": 0.10  # 10%
    }

    # Extract scores from JSON (normalized to 5)
    problem_score = (data["problem_statement"]["clarity"] + data["problem_statement"]["relevance"]) / 2
    solution_score = (data["solution"]["uniqueness"] + data["solution"]["feasibility"]) / 2
    business_model_score = data["business_model"]["scalability"]
    traction_score = 2 if data["traction"]["users"] > 0 else 0  # Simple binary traction check
    financials_score = 2 if data["financials"]["funding_raised"] > 0 else 0  # Funding presence check
    pitch_quality_score = (data["pitch_quality"]["design"] + data["pitch_quality"]["clarity"] + data["pitch_quality"]["engagement"]) / 3
    market_analysis_score = 4  # Assuming a reasonable score based on provided details
    team_score = 5 if len(data["team"]) >= 3 else 3  # Higher score for diverse, experienced teams

    # Normalize scores to 100 scale (assuming max score for each is 5)
    normalized_scores = {
        "problem_statement": (problem_score / 5) * 100,
        "solution": (solution_score / 5) * 100,
        "business_model": (business_model_score / 5) * 100,
        "traction": (traction_score / 5) * 100,
        "financials": (financials_score / 5) * 100,
        "pitch_quality": (pitch_quality_score / 5) * 100,
        "market_analysis": (market_analysis_score / 5) * 100,
        "team": (team_score / 5) * 100
    }

    # Compute weighted score
    overall_score = sum(normalized_scores[key] * weights[key] for key in weights)

    return round(overall_score, 2)  # Round to 2 decimal places


# 🔹 Generate Markdown Table
def generate_markdown_table(data):
    markdown = "# AirBed&Breakfast Pitch Evaluation\n\n"

    for category, details in data.items():
        markdown += f"## {category.replace('_', ' ').title()}\n\n"

        if isinstance(details, dict):
            markdown += "| Key | Value |\n"
            markdown += "| --- | ----- |\n"
            for key, value in details.items():
                markdown += f"| {key.replace('_', ' ').title()} | {format_value(value)} |\n"
        
        elif isinstance(details, list):
            if all(isinstance(item, dict) for item in details):
                headers = list(details[0].keys())
                markdown += "| " + " | ".join(headers) + " |\n"
                markdown += "| " + " | ".join(['-' * len(h) for h in headers]) + " |\n"

                for row in details:
                    markdown += "| " + " | ".join(format_value(row[h]) for h in headers) + " |\n"
            else:
                markdown += "- " + "\n- ".join(str(item) for item in details) + "\n"

        else:
            markdown += f"{format_value(details)}\n"

        markdown += "\n"

    return markdown

def format_value(value):
    """Formats values for better Markdown readability."""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)
import json


# 🔹 Chat with AI
def chat_with_ai(context, user_question):
    prompt = f"""
        You are an AI assistant specializing in startup analysis. Based on the user's analysis report, 
        provide insightful and relevant answers to their questions.

        **Analysis Report:**  
        {context}

        **User Question**  
        {user_question}

        Ensure that your response is **text-only**, preserving any tables using **Markdown format**.
    """

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt])

    return response.text
