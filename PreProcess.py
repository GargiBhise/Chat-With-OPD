import fitz

def get_pdf_text(pdf_docs):
    chunked_content = {}
    for pdf_doc in pdf_docs:
        chunk_id = 1
        doc = fitz.open(pdf_doc)
        page_no = 1
        for page in doc:
            text = page.get_text(opt="blocks")
            paragraph_no = 1
            for paragraph in text:
                chunked_content[chunk_id] = {'Page_Number' : page_no,
                                            'Paragraph_Number' : paragraph_no,
                                            'Content' : paragraph}
                paragraph_no += 1
    return chunked_content
