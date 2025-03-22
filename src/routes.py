import os
import json
from flask import Blueprint, request, jsonify
from services import convert_pdf_to_images, ocr_with_gemini, compute_pitch_score, generate_markdown_table
from models import get_llm_score
from config import INPUT_FOLDER, OUTPUT_FOLDER, EXTRACTION_OUTPUT_FOLDER

api_routes = Blueprint("api_routes", __name__)


# 📌 **Analyze Pitch Route**
@api_routes.route("/analyze", methods=["POST"])
def analyze_pitch():
    data = request.get_json()
    pdf_name = data.get("pdf_name", "")
    pdf_path = os.path.join("..",INPUT_FOLDER, pdf_name)
    output_folder = os.path.join("..",OUTPUT_FOLDER, pdf_name)

    image_paths = convert_pdf_to_images(pdf_path, output_folder)
    extracted_text = ocr_with_gemini(image_paths, "Maintain the table structure using Markdown.")

    os.makedirs(EXTRACTION_OUTPUT_FOLDER, exist_ok=True)
    output_text_file = os.path.join("..",EXTRACTION_OUTPUT_FOLDER, f"{pdf_name}_extracted.txt")

    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    output = get_llm_score(extracted_text)
    pitch_data = json.loads(output)
    pitch_score = compute_pitch_score(pitch_data)
    
    markdown_output = generate_markdown_table(pitch_data)

    return jsonify({"markdown_analysis": markdown_output, "pitch_score": f"{pitch_score}"})


# 📌 **Chat with AI**
@api_routes.route("/chat", methods=["POST"])
def conversation():
    data = request.get_json()
    context = data.get("context", "")
    user_question = data.get("prompt", "")

    from services import chat_with_ai
    response = chat_with_ai(context, user_question)

    return jsonify({"response": response})