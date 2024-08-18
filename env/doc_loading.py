import os
import re
from concurrent.futures import ThreadPoolExecutor
from langchain_community.document_loaders import PyPDFLoader

DATA_PATH = "data"

def clean_document(text):
    cleaned_text = re.sub(r'\s+', ' ', text)  
    cleaned_text = cleaned_text.strip()  
    return cleaned_text

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load_and_split()  
    return documents

def load_documents():
    
    pdf_files = [os.path.join(DATA_PATH, file_name) for file_name in os.listdir(DATA_PATH) if file_name.endswith(".pdf")]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(load_pdf, pdf_files))

    flat_documents = [doc for result in results for doc in result]

    cleaned_documents = []
    for doc in flat_documents:
        doc.page_content = clean_document(doc.page_content)  
        cleaned_documents.append(doc)
    
    return cleaned_documents

documents = load_documents()
