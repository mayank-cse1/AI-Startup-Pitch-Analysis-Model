import streamlit as st
import pandas as pd
import requests
import uuid
import time
from PyPDF2 import PdfReader
import os
import base64
from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
import pdfkit
import tempfile
from markdown_pdf import MarkdownPdf, Section
from config import INPUT_FOLDER, REPORT_FOLDER
st.set_page_config(layout="wide", page_title="PDF Analyzer & Chat")

# Initialize session state variables
temp_id = uuid.uuid4()
st.session_state.setdefault("id", temp_id)
st.session_state.setdefault("messages", [])
st.session_state.setdefault("analysis", "")
st.session_state.setdefault("score", None)
file_name = None
pdf_bytes = None
pdf_file = st.sidebar.file_uploader("Upload a PDF document", type=["pdf"], key="pdf_uploader")
# Sidebar for PDF Upload
st.sidebar.title("📂 Upload PDF File")


# Define folder to store uploaded PDFs
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{INPUT_FOLDER}"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists
REPORT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{REPORT_FOLDER}"))
os.makedirs(REPORT_FOLDER, exist_ok=True)  # Ensure folder exists
import os
import base64
import streamlit as st

# Convert and save Markdown as PDF
def convert_markdown_to_pdf(markdown_text):
    pdf = MarkdownPdf()
    pdf.meta["title"] = "Analysis Report"
    pdf.add_section(Section(markdown_text, toc=False))

    file_name = "Analysis_Report.pdf"
    output_path = os.path.join(REPORT_FOLDER, file_name)

    pdf.save(output_path)

    return output_path

if pdf_file:
    # Get the original file name
    file_name = pdf_file.name
    file_path = os.path.join(UPLOAD_FOLDER, file_name)  # Full path to save the file

    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(pdf_file.getbuffer())  # Save file content

    # Display PDF using streamlit_pdf_viewer
    with st.sidebar:
        pdf_viewer(file_path)

    # Send file name to Flask API for analysis
    flask_url = "http://127.0.0.1:5000/analyze"

    response = requests.post(flask_url, json={"pdf_name": file_name})
    # Handle API response
    if response.status_code == 200:
        st.session_state["analysis"] = response.json().get("markdown_analysis", "No analysis available.")
        st.session_state["score"] = response.json().get("pitch_score", "0")
    else:
        st.session_state["analysis"] = "Error fetching analysis!"
        st.session_state["score"] = "Error calculating pitch score"
    
st.markdown(
            "<h1 style='text-align: center;'>📊 PitchEvaluator: AI-Powered Startup Analysis</h1>", 
            unsafe_allow_html=True
        )

st.markdown(
    "<h3 style='text-align: center;'>🚀 Scoring & Analyzing Startup Pitches with AI Intelligence</h3>", 
    unsafe_allow_html=True
)
# Layout: Right column for markdown analysis
col1, col2 = st.columns([2, 3])

with col1:
    if st.session_state["score"]:
        st.markdown(
            f"<h1 style='text-align: center;'>📊 Pitch Score :: {st.session_state['score']}</h1>", 
            unsafe_allow_html=True
        )
    st.markdown(st.session_state["analysis"])
    if st.session_state["analysis"]:
        
        output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",f"output_reports/{file_name}"))  # Ensures absolute path usage
        
        pdf_path = convert_markdown_to_pdf(st.session_state["analysis"])

        with open(pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        
        # Provide a download button only when PDF is generated
        st.download_button(
            label="📥 Download Analysis Report",
            data=pdf_bytes,
            file_name="analysis_report.pdf",
            mime="application/pdf"
        )
    
    


# Display chat messages
for i, message in enumerate(st.session_state.get("messages", [])):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("💬 Ask about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Send user input to the Flask API
    chat_response = requests.post("http://127.0.0.1:5000/chat", json={"prompt": prompt, "context": st.session_state["analysis"]})
    
    assistant_response = "Sorry, I don't have an answer."
    if chat_response.status_code == 200:
        assistant_response = chat_response.json().get("response", assistant_response)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for word in assistant_response.split():
            full_response += word + " "
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.05)  # Simulated typing effect
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
