import PyPDF2

def extract_text(pdf_path):

    text = ""

    try:

        with open(pdf_path, "rb") as file:

            pdf_reader = PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:

        text = f"Error reading PDF: {e}"

    return text