import requests
from Bio import Entrez
import pandas as pd
import time

# Always tell NCBI who you are
Entrez.email = "aidshealthcare26@gmail.com"

def search_pubmed(query, max_results=10):
    """
    Search PubMed for research papers matching the query.
    Returns a pandas DataFrame of results.
    """
    try:
        # 1. Search for IDs
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()
        
        id_list = record["IdList"]
        if not id_list:
            return pd.DataFrame()
        
        # 2. Fetch details for these IDs
        handle = Entrez.efetch(db="pubmed", id=id_list, retmode="xml")
        papers = Entrez.read(handle)
        handle.close()
        
        results = []
        for pubmed_article in papers['PubmedArticle']:
            medline_citation = pubmed_article['MedlineCitation']
            article = medline_citation['Article']
            
            # Extract basic info
            pmid = str(medline_citation.get('PMID', ''))
            title = article.get('ArticleTitle', 'No title')
            
            # Extract Abstract
            abstract = 'No abstract available'
            if 'Abstract' in article and 'AbstractText' in article['Abstract']:
                abstract_texts = article['Abstract']['AbstractText']
                # AbstractText can be a list of strings (structured abstract)
                if isinstance(abstract_texts, list):
                    abstract = " ".join([str(text) for text in abstract_texts])
                else:
                    abstract = str(abstract_texts)
                    
            # Extract Publication Year
            year = 'Unknown'
            if 'Journal' in article and 'JournalIssue' in article['Journal']:
                pub_date = article['Journal']['JournalIssue'].get('PubDate', {})
                year = pub_date.get('Year', year)
                
            results.append({
                'ID': pmid,
                'Title': title,
                'Abstract': abstract,
                'Year': year,
                'Source': 'PubMed',
                'URL': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            })
            
        return pd.DataFrame(results)
        
    except Exception as e:
        print(f"Error fetching from PubMed: {e}")
        # Return empty DataFrame on failure
        return pd.DataFrame()

# Fallback mock search for reliability
def mock_search(query):
    """
    Provides mock search results if API fails or for demo purposes.
    """
    time.sleep(1.5)  # Simulate network latency
    mock_data = [
        {
            'ID': '101', 'Title': f"A randomized controlled trial of interventions for {query}",
            'Abstract': "This study investigates the efficacy of the intervention on 500 patients. Results indicate a significant positive effect (p < 0.05).",
            'Year': '2023', 'Source': 'MockDB', 'URL': '#'
        },
        {
            'ID': '102', 'Title': f"Systematic review of {query} in clinical settings",
            'Abstract': "We reviewed 50 studies. The intervention showed moderate improvements compared to placebo but had a high variance in outcomes.",
            'Year': '2022', 'Source': 'MockDB', 'URL': '#'
        },
        {
            'ID': '103', 'Title': f"Adverse effects and meta-analysis of {query}",
            'Abstract': "A comprehensive analysis of adverse effects. Finding no significant difference in mortality rates but a slight increase in minor side effects.",
            'Year': '2024', 'Source': 'MockDB', 'URL': '#'
        },
        {
            'ID': '104', 'Title': f"Case study on {query} application",
            'Abstract': "A single patient case emphasizing the protocol. Not highly relevant for a broad quantitative meta-analysis.",
            'Year': '2021', 'Source': 'MockDB', 'URL': '#'
        }
    ]
    return pd.DataFrame(mock_data)

def get_papers(query, max_results=10, use_mock=False):
    if use_mock:
        return mock_search(query), False
    
    df = search_pubmed(query, max_results)
    if df.empty:
        # Fallback to mock if API returns nothing or internet fails entirely
        return mock_search(query), True
    return df, False
