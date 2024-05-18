# PreProcess.py

import os
import requests
from urllib.parse import urlparse, unquote
import fitz  # PyMuPDF
from tqdm.auto import tqdm

def get_filename_from_url(url):
    """ Extracts the filename from the URL and ensures it ends with .pdf"""
    parsed_url = urlparse(url)
    filename = os.path.basename(unquote(parsed_url.path))
    if not filename:
        filename = "downloaded_file.pdf"
    elif not filename.lower().endswith('.pdf'):
        filename += ".pdf"
    return filename

def download_pdf(download_folder, url):
    """ Downloads a PDF from a URL and saves it to a specified folder """
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    filename = get_filename_from_url(url)
    local_path = os.path.join(download_folder, filename)

    if not os.path.exists(local_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, "wb") as file:
                file.write(response.content)
            return local_path
        else:
            raise Exception(f"Failed to download the file. Status code: {response.status_code}")
    return local_path

def text_formatter(text: str) -> str:
    """ Performs minor formatting on text """
    cleaned_text = text.replace("\n", " ").strip()
    return cleaned_text

def open_and_read_pdf(pdf_path: str) -> list:
    """ Opens a PDF and reads its content into a list of dictionaries """
    doc = fitz.open(pdf_path)
    pages_and_texts = []
    for page_number, page in tqdm(enumerate(doc)):
        text = page.get_text()
        text = text_formatter(text)
        pages_and_texts.append({"page_number": page_number,
                                "page_char_count": len(text),
                                "page_word_count": len(text.split(" ")),
                                "page_sentence_count_raw": len(text.split(". ")),
                                "page_token_count": len(text) / 4,  # 1 token = ~4 characters
                                "text": text})
    return pages_and_texts
