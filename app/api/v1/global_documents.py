from fastapi import APIRouter, UploadFile, File

from app.engines.document_processor import (
    extract_text_from_pdf,
    create_chunks
)

from app.services.vector_store import (
    save_global_chunks
)

import os

router = APIRouter()

UPLOAD_DIR = "uploads/global"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/global/documents")
async def upload_global_document(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    text = extract_text_from_pdf(
        file_path
    )

    chunks = create_chunks(
        text
    )

    save_global_chunks(
        file.filename,
        chunks
    )

    return {
        "status": "success",
        "chunks": len(chunks),
        "file": file.filename
    }