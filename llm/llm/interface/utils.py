import pdfplumber

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
#results = extract_text_from_pdf('/Users/new/Downloads/Dare_to_Discipline.pdf')
#print(results)