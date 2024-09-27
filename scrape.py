import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from utils import clean_text

def scrape_resume(keywords):
    try:
        query = f"resumes for {keywords}"
        response = requests.get(f"https://www.google.com/search?q={query}", timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True)][:2]
    except requests.exceptions.Timeout:
        print("Timed out")
        return []

def fetch_url_content(url):
    try:
        loader = WebBaseLoader(url)
        data = clean_text(loader.load().pop().page_content)
        return data
    except Exception as e:
        print(f"Failed to retrieve data from {url}: {e}")
        return ""