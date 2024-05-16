'''Data Ingestion and Pre-Processing Module'''

import os
import requests
import fitz 

def download_pdf(pdf_path, url):
    if not os.path.exists(pdf_path):
        print(f"[INFO] File doesn't exist, downloading from {url}...")

        response = requests.get(url)

        if response.status_code == 200:
            with open(pdf_path, "wb") as file:
                file.write(response.content)
            print(f"[INFO] The file has been downloaded and saved as {pdf_path}")
        else:
            print(f"[ERROR] Failed to download the file. Status code: {response.status_code}")
            return False
    else:
        print(f"File {pdf_path} exists.")
    return True

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

'''Method that returns a Dictionary containing chunked text with metadata'''
# def get_pdf_text(pdf_docs):
#     chunked_content = {}
#     for pdf_doc in pdf_docs:
#         chunk_id = 1
#         doc = fitz.open(pdf_doc)
#         page_no = 1
#         for page in doc:
#             text = page.get_text(opt="blocks")
#             paragraph_no = 1
#             for paragraph in text:
#                 chunked_content[chunk_id] = {'Page_Number' : page_no,
#                                             'Paragraph_Number' : paragraph_no,
#                                             'Content' : paragraph}
#                 paragraph_no += 1
#     return chunked_content
