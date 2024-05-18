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

# def extract_text_from_pdf(pdf_path):
#     """
#     Extracts text from a PDF file
#     """
#     # Initialize an empty string to hold the text
#     text = ""
#     # Open the PDF file
#     with fitz.open(pdf_path) as doc:
#         # For each page in the document
#         for page in doc:
#             # Add the text of the page to the string
#             text += page.get_text()
#     # Return the extracted text
#     return text
def text_formatter(text: str) -> str:
     """Performs minor formatting on text."""
     cleaned_text = text.replace("\n", " ").strip()
     return cleaned_text

def open_and_read_pdf(pdf_path: str) -> list[dict]:
    print("Begin process_files method.")
    doc = fitz.open(pdf_path)
    pages_and_texts = []
    for page_number, page in enumerate(doc):
        text = page.get_text()
        text = text_formatter(text)
        pages_and_texts.append({"page_number": page_number,
                                "page_char_count": len(text),
                                "page_word_count": len(text.split(" ")),
                                "page_sentence_count_raw": len(text.split(". ")),
                                "page_token_count": len(text) / 4, # 1 token = ~4 character
                                "text": text})
    print("Finished process_files method.")
    return pages_and_texts
