# AI for Automated Systematic Reviews and Meta-Analysis

This repository contains our submission for **Problem Statement Number – 6** of the Medathon hackathon.

It is a complete end-to-end Python pipeline using Streamlit that automates:
1. Searching for relevant medical literature via the PubMed API.
2. Abstract screening (Include/Exclude) using Large Language Models (LLMs).
3. Data extraction (Samples, Effect Sizes, Margins) via LLMs.
4. Auto-generation of a Meta-Analysis Forest Plot and AI System Review Conclusion.

## Setup Instructions

1. **Clone the repository:**
```bash
git clone <your-repository-url>
cd Medathon
```

2. **Install Python dependencies:**
Make sure you have Python 3.8+ installed. Run:
```bash
pip install -r requirements.txt
```

3. **Run the Application:**
```bash
streamlit run app.py
```

## How It Works

This project features a **Hybrid Execution Model**:
- If you supply a `GEMINI_API_KEY` in the sidebar, the application makes live calls to Google's Generative AI models.
- If you run it locally without a key (or if the API drops), the system gracefully degrades to a Mock Generator mode. This ensures that the Meta-Analysis extraction code and data-viz pipelines can still be demonstrated flawlessly.

## Stack
- **Frontend Layer:** `streamlit`
- **Data Query Layer:** `biopython` and `requests`
- **AI/LLM Layer:** `google-generativeai`
- **Analytics Layer:** `pandas`, `numpy`, `matplotlib`
