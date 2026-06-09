from fastapi import APIRouter, UploadFile, File
from app.engines.document_processor import extract_text_from_pdf
import os

router = APIRouter()

DOCUMENTS = {}

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/projects/{project_id}/documents")
async def upload_document(
    project_id: str,
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    extracted_text = ""

    if file.filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(
            file_path
        )

    if project_id not in DOCUMENTS:
        DOCUMENTS[project_id] = []

    DOCUMENTS[project_id].append({
        "filename": file.filename,
        "size": len(content),
        "text": extracted_text[:500]
    })

    return {
        "status": "success",
        "project_id": project_id,
        "filename": file.filename,
        "preview": extracted_text[:500]
    }


@router.get("/projects/{project_id}/documents")
def get_documents(project_id: str):

    return DOCUMENTS.get(project_id, [])