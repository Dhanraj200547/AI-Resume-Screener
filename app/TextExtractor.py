import fitz  # PyMuPDF library for PDF handling

async def extract_text_from_pdf(uploaded_file):
    contents = await uploaded_file.read()
    pdf_doc = fitz.open(stream=contents, filetype="pdf")
    text = ""
    for page in pdf_doc:
        text += page.get_text()
    return text