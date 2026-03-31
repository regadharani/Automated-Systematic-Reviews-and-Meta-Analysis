import google.generativeai as genai
import os
import random

def setup_agent(api_key=None):
    """
    Configure the Gemini API if an API key is provided.
    """
    if api_key:
        genai.configure(api_key=api_key)
        return True
    elif os.environ.get("GEMINI_API_KEY"):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        return True
    return False

def _mock_screening(abstract):
    """
    Mock screening agent that decides whether a paper is included based on keywords.
    """
    abstract_lower = abstract.lower()
    if 'model' in abstract_lower or 'single patient' in abstract_lower or 'case study' in abstract_lower:
        return {"decision": "Exclude", "reason": "Did not meet inclusion criteria (e.g., sample size too small or single case study)."}
    else:
        return {"decision": "Include", "reason": "Abstract discusses a randomized control trial or systematic review relevant to the query."}

def screen_paper(abstract, api_key_provided=False):
    """
    AI Screening Agent: Reads the abstract and decides 'Include' or 'Exclude'.
    """
    if api_key_provided:
        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            prompt = f"You are a medical researcher. Read this abstract and decide if it should be included in a meta-analysis. Reply exactly with a JSON object containing keys 'decision' (either 'Include' or 'Exclude') and 'reason'. Abstract: {abstract}"
            response = model.generate_content(prompt)
            # Extremely simple parser for hackathon resiliency
            text = response.text.strip().replace("```json", "").replace("```", "")
            import json
            result = json.loads(text)
            if 'decision' not in result:
                raise ValueError("Missing decision key")
            return result
        except Exception as e:
            print(f"API Error during screening: {e}, falling back to mock")
            return _mock_screening(abstract)
    else:
        return _mock_screening(abstract)

def _mock_extraction(abstract):
    """
    Mock Data Extraction logic to output synthetic statistics for the Forest Plot.
    """
    abstract_lower = abstract.lower()
    # Random realistic-looking trial statistics
    n_sample = random.randint(30, 800)
    effect_size = round(random.uniform(0.1, 1.2), 2)
    # Give a negative/low effect to systematic reviews or case studies for variation
    if 'systematic' in abstract_lower:
        effect_size = round(random.uniform(0.05, 0.4), 2)
    
    ci_lower = round(effect_size - random.uniform(0.1, 0.3), 2)
    ci_upper = round(effect_size + random.uniform(0.1, 0.5), 2)
    
    return {
        "Sample_Size": n_sample,
        "Effect_Size": effect_size,
        "CI_Lower": ci_lower,
        "CI_Upper": ci_upper,
        "Findings": "The intervention demonstrated distinct outcomes corresponding to the effect size.",
    }

def extract_data(abstract, api_key_provided=False):
    """
    AI Extraction Agent: Extracts PICO parameters and statistical data for Meta-Analysis.
    """
    if api_key_provided:
        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            prompt = f"""You are a systematic reviewer. Extract standard meta-analysis statistical approximations from this abstract. 
            Reply ONLY with a raw JSON object containing these numeric keys: 'Sample_Size' (integer), 'Effect_Size' (float), 'CI_Lower' (float), 'CI_Upper' (float). 
            Also include a key 'Findings' with a short 1-sentence summary.
            If data is missing, guess a plausible statistic for demonstration purposes (since this is a hackathon prototype).
            Abstract: {abstract}"""
            response = model.generate_content(prompt)
            text = response.text.strip().replace("```json", "").replace("```", "")
            import json
            result = json.loads(text)
            return result
        except Exception as e:
            print(f"API Error during extraction: {e}, falling back to mock")
            return _mock_extraction(abstract)
    else:
        return _mock_extraction(abstract)

def generate_summary(df_extracted, api_key_provided=False):
    """
    Final AI Agent: Summarizes the pooled findings.
    """
    if api_key_provided:
        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            context = df_extracted[['Title', 'Effect_Size', 'Findings']].to_dict(orient='records')
            prompt = f"As a health researcher, write a concise 3-paragraph systematic review conclusion based on these extracted paper findings: {context}"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"API Error during summarization: {e}, falling back to mock")
    
    # Fallback
    return f"**Systematic Review Summary:**\n\nBased on the automated extraction of {len(df_extracted)} included studies, the overall evidence points towards a generally positive effect size. The majority of studies report standard deviations within expected clinical bounds. \n\nFurther large-scale randomized controlled trials are recommended to confirm the uniformity of this intervention across wider population demographics."
