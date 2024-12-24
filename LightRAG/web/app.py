from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import sys
import os

# Add parent directory to path so we can import from lightrag
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lightrag.main import LightRAG

app = Flask(__name__)
light_rag = None

def init_light_rag():
    global light_rag
    if light_rag is None:
        light_rag = LightRAG()

@app.route('/')
def home():
    return render_template('index.html')

def ingest_company_data(url):
    """
    Scrapes and processes company data from URL
    """
    try:
        # Define pages to scrape
        pages_to_scrape = [
            "",  # Homepage
            "about",
            "company",
            "products",
            "solutions",
            "careers"
        ]
        
        all_content = []
        for page in pages_to_scrape:
            try:
                full_url = urljoin(url, page)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(full_url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract relevant content
                content = {
                    'url': full_url,
                    'title': soup.title.string if soup.title else '',
                    'main_content': ' '.join([p.text for p in soup.find_all('p')]),
                    'headings': ' '.join([h.text for h in soup.find_all(['h1', 'h2', 'h3'])])
                }
                all_content.append(content)
            except Exception as e:
                print(f"Error scraping {full_url}: {str(e)}")
                
        return all_content
                
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None

def update_graph_with_company(company_data):
    """
    Updates the knowledge graph with new company information
    """
    init_light_rag()
    
    # Combine all content into a single document
    combined_content = ""
    for page in company_data:
        combined_content += f"\nPage: {page['url']}\n"
        combined_content += f"Title: {page['title']}\n"
        combined_content += f"Content: {page['main_content']}\n"
        combined_content += f"Headings: {page['headings']}\n"
    
    # Process through LightRAG
    light_rag.process_document(combined_content)
    return True

@app.route('/api/analyze_company', methods=['POST'])
def analyze_company():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
        
    # Scrape and process company data
    company_data = ingest_company_data(url)
    
    if not company_data:
        return jsonify({'error': 'Failed to scrape company data'}), 500
    
    # Update graph
    try:
        update_graph_with_company(company_data)
    except Exception as e:
        return jsonify({'error': f'Failed to update graph: {str(e)}'}), 500
    
    # Return analysis
    return jsonify({
        'status': 'success',
        'company_data': company_data
    })

# For local development
if __name__ == '__main__':
    app.run(debug=True)
