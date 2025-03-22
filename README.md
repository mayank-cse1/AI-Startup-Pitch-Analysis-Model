# AI-Startup-Pitch-Analysis-Model

## Objective

The Pitch Analysis App is an **AI-powered tool** designed to evaluate startup pitch documents. Using **Google Gemini API**, the app extracts insights from **OCR-extracted text** and provides structured feedback on various business aspects.

This script evaluates a **startup pitch deck** based on **eight key criteria** and assigns a final score out of **100**. Each criterion has a **weighted contribution**, ensuring a balanced assessment of the startup’s potential.

## Dataset & Inputs
- A set of sample pitch decks.
- AI model must extract and analyze key sections: **Problem, Solution, Market, Business Model, Financials, Team**.


## Tasks

### 1. Text Extraction & Preprocessing
- Use **OCR or PDF parsing** to extract text from pitch decks.
- Preprocess text by removing unnecessary elements and formatting.

### 2. Feature Engineering
- Identify key sections from a pitch deck.
- Assign weights based on the importance of different sections.

### 3. Scoring Model
- Utilize **LLM-based evaluation** (GPT/Gemini API or fine-tuned BERT model) to analyze the quality of each section.
- Generate a **pitch score (0-100)** based on predefined metrics.

### 4. Strength & Weakness Analysis
- Provide **personalized feedback** on areas that need improvement.
- Suggest content improvements or additional data needed.

### 5. Output
- Display **pitch score** along with AI-generated **feedback** on strengths and weaknesses.

## 📊 Scoring Criteria  
The scoring system considers the following aspects:

| **Criterion**        | **Weight (%)** | **Description** |
|----------------------|--------------|---------------|
| **Problem Statement**  | 15%  | Measures the clarity and relevance of the problem being solved. |
| **Solution**          | 20%  | Evaluates uniqueness and feasibility of the proposed solution. |
| **Business Model**    | 10%  | Assesses scalability and sustainability of the business. |
| **Traction**         | 10%  | Checks user growth and adoption (e.g., based on user count). |
| **Financials**       | 10%  | Analyzes funding raised and financial stability. |
| **Pitch Quality**    | 10%  | Evaluates design, clarity, and engagement in presentation. |
| **Market Analysis**  | 15%  | Looks at competition and market positioning. |
| **Team**            | 10%  | Considers the experience and diversity of the team. |

---

## 🔢 Score Calculation  
Each category is **scored out of 5**, then **normalized to 100** and **weighted accordingly**.  

### **Key Features in Score Computation**  
✅ **Handles missing JSON fields safely**  
✅ **Scales traction based on actual user count**  
✅ **Normalizes financials with funding thresholds**  
✅ **Assesses market analysis by competitor count**  
✅ **Provides a realistic team evaluation based on size**  

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Additional System Packages (Linux Users)
```bash
sudo apt update && sudo apt install -y poppler-utils
```

### 3. Run the Backend
```bash
python app.py
```

### 4. Run the UI
Open another terminal and execute:
```bash
streamlit run ui.py
```

## Project Structure
```
AI-Pitch-Analysis
│── app.py          # Main application entry point
│── model.py        # LLM-based scoring model implementation
│── ui.py           # Streamlit UI for pitch evaluation
│── routes.py       # API routes
│── services.py     # Business logic for processing pitch decks
│── requirements.txt # Python dependencies
└── README.md       # Project documentation
```



## 🛠️ Usage  
1. **Upload your pitch PDF** (e.g., startup details).  
2. **Run the script** to compute the pitch score.  
3. **Get a score out of 100** with insights into key strengths and weaknesses.  

---

## 📌 Example Output  
```
Overall Pitch Score: 78.5/100
```

## Future Enhancements
- **Fine-tune the scoring model** for more accurate pitch evaluation.
- **Improve OCR accuracy** for better text extraction.
- **Integrate more AI models** for better feedback and analysis.

## License
This project is open-source under the MIT License.

---
Feel free to modify and extend the project as needed! 🚀

