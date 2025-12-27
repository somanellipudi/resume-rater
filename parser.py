from pypdf import PdfReader
from docx import Document
from bs4 import BeautifulSoup
import requests

def parse_pdf(file):
    reader = PdfReader(file)
    return " ".join(p.extract_text() or "" for p in reader.pages)

def parse_docx(file):
    doc = Document(file)
    return " ".join(p.text for p in doc.paragraphs)

def parse_url(url):
    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(" ")
    
