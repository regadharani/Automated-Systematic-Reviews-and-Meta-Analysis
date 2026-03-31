# AI for Automated Systematic Reviews and Meta-Analysis

**Hackathon Problem Statement:** Number – 6
**Submission Email:** aidshealthcare26@gmail.com

---

## Abstract
Systematic reviews and meta-analyses are the gold standard for evidence-based medicine, yet the manual process of screening, extracting data, and synthesizing results from thousands of papers is labor-intensive and error-prone. 

Our solution is an **End-to-End AI-driven Pipeline** that automates the entirety of the systematic review process. Given a research query, the system autonomously fetches relevant literature from databases, utilizes Large Language Models (LLMs) to screen abstracts based on inclusion criteria, extracts vital statistical parameters (e.g., sample sizes, effect sizes), and generates a consolidated meta-analysis forest plot alongside a narrative summary.

## Proposed Architecture
The project is built on a modular Python architecture comprising 4 main pipelines:

1. **Search API Module (`search_engine.py`)**: Fetches raw data by interacting directly with the PubMed API (via Biopython) to collect PMIDs, titles, and structural abstracts.
2. **AI Screening Agent (`ai_agent.py`)**: Prompts an LLM (such as Gemini 1.5 Pro) to parse the unstructured abstract and classify papers as `Include/Exclude` based on strict logical criteria, avoiding human bias.
3. **AI Extraction Agent (`ai_agent.py`)**: Analyzes the included papers to formulate synthetic structured data points like Population Size, Effect Rate, and Confidence Intervals.
4. **Meta-Analysis Module (`meta_analysis.py`)**: Aggregates the extracted datasets using `pandas` and computes pooled meta-statistics, rendering a visualization (Forest Plot) via `matplotlib`.

## The "Hybrid" Fallback Advantage (Tech Choice)
During hackathons and live research deployments, network APIs and LLM rate constraints can cause critical failures. 
Our codebase implements a **Hybrid Execution Model**:
- **Live Mode**: If an API key is provided, the system interfaces live with Google Generative AI to compute unstructured-to-structured inferences.
- **Mock/Offline Mode**: In the absence of an API key or during network drops, the application seamlessly delegates execution to a mock synthetic data provider. This ensures **guaranteed reproducibility** and demonstrates robust fault-tolerant software engineering.

## Installation & Reproducibility (GitHub Link)

The source code and documentation are available on GitHub.

**Repository Link:** [Insert your GitHub Repository URL here]

### To run locally:
```bash
# 1. Clone your repository
git clone <repository_url>

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Launch the Application
streamlit run app.py
```

## Future Scope
- **Full-text Processing:** Evolving the LLM context limits to parse full-text PDFs instead of just abstracts.
- **Advanced Statistical Models:** Migrating from unweighted average effect sizes to properly applying fixed-effect or random-effects statistical frameworks (e.g., using specialized Python meta-analysis libraries).
- **Automated Protocol Registration:** Connecting directly to PROSPERO to automatically register the analysis protocol.
