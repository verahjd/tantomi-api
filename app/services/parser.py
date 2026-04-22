import fitz #PyMuPDF

def extract_text_from_pdf(contents: bytes) -> str:
    text = ""
    with fitz.open(stream=contents, filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text