import streamlit as st
import pandas as pd
import time

from search_engine import get_papers
from ai_agent import setup_agent, screen_paper, extract_data, generate_summary
from meta_analysis import create_forest_plot

st.set_page_config(page_title="AI Systematic Review & Meta-Analysis", layout="wide")

st.title("🤖 AI for Automated Systematic Reviews and Meta-Analysis")
st.markdown("""
Welcome to the Automated Systematic Review system. 
Enter a clinical query below, and this system will:
1. **Search** for papers from standard databases.
2. **Screen** abstracts for relevance using AI.
3. **Extract** trial data (PICO / Statistics).
4. **Analyze** the pooled findings in a Meta-Analysis Forest Plot.
""")

st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Gemini API Key (Optional for real LLM)", type="password")
use_mock_search = st.sidebar.checkbox("Use Offline Mock Data", value=True)

# Set up agent based on key
api_key_provided = setup_agent(api_key)
if api_key_provided:
    st.sidebar.success("AI Agent configured properly.")
else:
    st.sidebar.info("Running in Mock AI fallback mode.")

# Session State for tracking pipeline progress
if 'df_papers' not in st.session_state:
    st.session_state['df_papers'] = None
if 'df_screened' not in st.session_state:
    st.session_state['df_screened'] = None
if 'df_extracted' not in st.session_state:
    st.session_state['df_extracted'] = None

query = st.text_input("Research Query:", value="Efficacy of cognitive behavioral therapy for insomnia")

if st.button("Start Systematic Review Pipeline"):
    # Step 1: SEARCH
    with st.spinner("Step 1: Searching for literature..."):
        df_papers, was_fallback = get_papers(query, max_results=10, use_mock=use_mock_search)
        st.session_state['df_papers'] = df_papers
        time.sleep(1) # just for UI feeling
    
    if was_fallback and not use_mock_search:
        st.warning("⚠️ Internet or Search API limit reached! Automatically switched to the robust Offline Mock Dataset so your presentation can continue without crashing.")
    
    if st.session_state['df_papers'].empty:
        st.error("No papers found. Try adjusting your query or toggle mock data.")
        st.stop()
        
    st.success(f"Found {len(st.session_state['df_papers'])} potential papers.")
    st.dataframe(st.session_state['df_papers'][['Title', 'Year', 'Source']])
    
    st.markdown("### Read the Papers")
    for idx, row in st.session_state['df_papers'].iterrows():
        with st.expander(f"📄 {row['Title']} ({row['Year']})"):
            st.markdown(f"**Source:** {row['Source']}")
            st.markdown(f"**Abstract:** {row['Abstract']}")
            st.markdown(f"[Link to Publication]({row['URL']})")
    
    # Step 2: SCREENING
    st.subheader("AI Abstract Screening")
    with st.spinner("Step 2: AI Agent reading abstracts to determine inclusion..."):
        screened_records = []
        for idx, row in st.session_state['df_papers'].iterrows():
            decision_obj = screen_paper(row['Abstract'], api_key_provided=api_key_provided)
            row_dict = row.to_dict()
            row_dict['Inclusion'] = decision_obj.get('decision', 'Exclude')
            row_dict['Reason'] = decision_obj.get('reason', 'N/A')
            screened_records.append(row_dict)
        st.session_state['df_screened'] = pd.DataFrame(screened_records)
    
    included_df = st.session_state['df_screened'][st.session_state['df_screened']['Inclusion'] == 'Include']
    st.write(f"Papers Included: {len(included_df)} / {len(st.session_state['df_screened'])}")
    st.dataframe(st.session_state['df_screened'][['Title', 'Inclusion', 'Reason']])
    
    if included_df.empty:
        st.error("No papers passed the inclusion criteria. Meta-analysis cannot proceed.")
        st.stop()
        
    # Step 3: EXTRACTION
    st.subheader("Data Extraction")
    with st.spinner("Step 3: AI Extracting trial statistics from Included Papers..."):
        extracted_records = []
        for idx, row in included_df.iterrows():
            extracted_obj = extract_data(row['Abstract'], api_key_provided=api_key_provided)
            row_dict = row.to_dict()
            # Merge extracted
            row_dict.update(extracted_obj)
            extracted_records.append(row_dict)
            
        st.session_state['df_extracted'] = pd.DataFrame(extracted_records)
        
    st.dataframe(st.session_state['df_extracted'][['Title', 'Sample_Size', 'Effect_Size', 'CI_Lower', 'CI_Upper', 'Findings']])
    
    # Step 4: META-ANALYSIS & SUMMARY
    st.subheader("Final Meta-Analysis")
    with st.spinner("Generating Meta-Analysis Forest Plot and AI Report..."):
        # Plot
        fig = create_forest_plot(st.session_state['df_extracted'])
        col1, col2 = st.columns([1, 1])
        with col1:
            st.pyplot(fig)
            
        with col2:
            st.markdown("### AI Generated Conclusion")
            summary = generate_summary(st.session_state['df_extracted'], api_key_provided=api_key_provided)
            st.info(summary)
            
    st.success("Systematic Review Pipeline Completed Successfully!")
