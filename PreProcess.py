import os
import requests
from urllib.parse import urlparse, unquote
import fitz  # PyMuPDF

def get_filename_from_url(url):
    """ Extracts the filename from the URL and ensures it ends with .pdf"""

    # Parse the URL into components
    parsed_url = urlparse(url)
    # Extract the base name of the URL (the part after the last slash)
    filename = os.path.basename(unquote(parsed_url.path))
    if not filename:
        # If the URL doesn't specify a filename, use a default one
        filename = "downloaded_file.pdf"
    elif not filename.lower().endswith('.pdf'):
        # If the filename doesn't end with .pdf, add it
        filename += ".pdf"
    return filename

def download_pdf(download_folder, url):
    """
    Downloads a PDF from a URL and saves it to a specified folder
    """
    # If the download folder doesn't exist, create it
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Get the filename from the URL
    filename = get_filename_from_url(url)
    # Create the local path for the downloaded file
    local_path = os.path.join(download_folder, filename)

    # If the file doesn't already exist, download it
    if not os.path.exists(local_path):
        # Send a GET request to the URL
        response = requests.get(url)
        # If the request is successful, save the content to a file
        if response.status_code == 200:
            with open(local_path, "wb") as file:
                file.write(response.content)
            # Return the local path if download is successful
            return local_path
        else:
            # If the request is not successful, raise an exception
            raise Exception(f"Failed to download the file. Status code: {response.status_code}")
    # If the file already exists, return its local path
    return local_path

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file
    """
    # Initialize an empty string to hold the text
    text = ""
    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        # For each page in the document
        for page in doc:
            # Add the text of the page to the string
            text += page.get_text()
    # Return the extracted text
    return text


