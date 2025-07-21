import os
import fitz  # PyMuPDF for PDFs
import docx
from typing import Union, List


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs).strip()


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def clean_text(text: str) -> str:
    return text.replace("\xa0", " ").replace("\n\n", "\n").strip()


async def process_document_extraction(
        file_path: str,
        collection_name: str = None,
        workflow_id: str = None,
) -> Union[str, List[str]]:
    """
    Extracts text from a document (PDF, DOCX, TXT).

    Args:
        file_path (str): Path to uploaded document.
        collection_name (str): Collection to which the data is related.
        workflow_id (str): Workflow ID, for tagging or metadata.

    Returns:
        str or list of strings: Cleaned and extracted text ready for vector ingestion.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        raw_text = extract_text_from_docx(file_path)
    elif ext == ".txt":
        raw_text = extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    cleaned_text = clean_text(raw_text)

    # Optional: split text into chunks if needed for vector DB
    # Example naive chunking:
    chunk_size = 1000
    chunks = [cleaned_text[i:i + chunk_size] for i in range(0, len(cleaned_text), chunk_size)]

    return chunks if len(chunks) > 1 else [cleaned_text]
