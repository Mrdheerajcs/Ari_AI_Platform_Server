from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(
    file_path
):

    reader = PdfReader(
        file_path
    )

    text = ""

    for page in reader.pages:

        text += (
            page.extract_text()
            or ""
        )

    return text


def extract_text_from_docx(
    file_path
):

    document = Document(
        file_path
    )

    text = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text.append(
                paragraph.text
            )

    return "\n".join(
        text
    )


def create_chunks(
    text: str,
    chunk_size: int = 500
):

    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):

        chunks.append(
            text[
                i:i + chunk_size
            ]
        )

    return chunks