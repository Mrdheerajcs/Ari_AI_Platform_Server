from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    Query
)
from fastapi.responses import FileResponse

from app.core.security import authenticate_api
from app.core.database import engine

from app.engines.document_processor import (
    extract_text_from_pdf,
    extract_text_from_docx,
    create_chunks
)

from app.services.vector_store import save_chunks

from sqlalchemy import text
from datetime import datetime
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/projects/{project_id}/documents")
async def upload_document(
    project_id: str,
    file: UploadFile = File(...),
    user=Depends(authenticate_api)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    extracted_text = ""

    if file.filename.lower().endswith(".pdf"):

        extracted_text = extract_text_from_pdf(
            file_path
        )

    elif file.filename.lower().endswith(".docx"):

        extracted_text = extract_text_from_docx(
            file_path
        )

    chunks = []

    if extracted_text:

        chunks = create_chunks(
            extracted_text
        )

        save_chunks(
            project_id=project_id,
            document_name=file.filename,
            chunks=chunks
        )

    document_type = "pdf"

    if file.filename.lower().endswith(".docx"):
        document_type = "docx"

    elif file.filename.lower().endswith(".txt"):
        document_type = "txt"

    elif file.filename.lower().endswith(".html"):
        document_type = "html"

    elif file.filename.lower().endswith(".md"):
        document_type = "md"

    with engine.begin() as conn:

        project = conn.execute(
            text(
                """
                SELECT id
                FROM projects
                WHERE project_id = :project_id
                """
            ),
            {
                "project_id": project_id
            }
        ).fetchone()

        if not project:

            return {
                "status": "error",
                "message": "Project not found"
            }

        conn.execute(
            text(
                """
                INSERT INTO project_documents
                (
                    project_id,
                    document_name,
                    document_type,
                    s3_path,
                    chunk_count,
                    status,
                    uploaded_at,
                    file_size
                )
                VALUES
                (
                    :project_id,
                    :document_name,
                    :document_type,
                    :s3_path,
                    :chunk_count,
                    :status,
                    :uploaded_at,
                    :file_size
                )
                """
            ),
            {
                "project_id": project.id,
                "document_name": file.filename,
                "document_type": document_type,
                "s3_path": file_path,
                "chunk_count": len(chunks),
                "status": "completed",
                "uploaded_at": datetime.utcnow(),
                "file_size": len(content)
            }
        )

    return {
        "status": "success",
        "project_id": project_id,
        "filename": file.filename,
        "document_type": document_type,
        "file_size": len(content),
        "chunks_created": len(chunks),
        "preview": extracted_text[:500]
    }


@router.get("/projects/{project_id}/documents/{document_id}")
def get_document_details(
    project_id: str,
    document_id: int,
    user=Depends(authenticate_api)
):

    with engine.connect() as conn:

        result = conn.execute(
            text(
                """
                SELECT
                    pd.id,
                    p.project_id AS project_code,
                    pd.document_name,
                    pd.document_type,
                    pd.s3_path,
                    pd.chunk_count,
                    pd.status,
                    pd.uploaded_at,
                    pd.processed_at,
                    pd.file_size,
                    pd.vector_collection_name,
                    pd.error_message
                FROM project_documents pd
                JOIN projects p
                    ON p.id = pd.project_id
                WHERE p.project_id = :project_id
                AND pd.id = :document_id
                """
            ),
            {
                "project_id": project_id,
                "document_id": document_id
            }
        ).fetchone()

        if not result:

            return {
                "status": "error",
                "message": "Document not found"
            }

        return dict(result._mapping)


@router.get("/projects/{project_id}/documents/{document_id}/view")
def view_document(
    project_id: str,
    document_id: int,
    user=Depends(authenticate_api)
):

    with engine.connect() as conn:

        result = conn.execute(
            text(
                """
                SELECT
                    pd.document_name,
                    pd.s3_path
                FROM project_documents pd
                JOIN projects p
                    ON p.id = pd.project_id
                WHERE p.project_id = :project_id
                AND pd.id = :document_id
                """
            ),
            {
                "project_id": project_id,
                "document_id": document_id
            }
        ).fetchone()

        if not result:

            return {
                "status": "error",
                "message": "Document not found"
            }

        if not os.path.exists(result.s3_path):

            return {
                "status": "error",
                "message": "File not found on disk"
            }

        return FileResponse(
            path=result.s3_path,
            filename=result.document_name
        )


@router.get("/documents/view-by-path")
def view_document_by_path(
    path: str = Query(...),
    user=Depends(authenticate_api)
):

    if not os.path.exists(path):

        return {
            "status": "error",
            "message": "File not found"
        }

    return FileResponse(
        path=path,
        filename=os.path.basename(path)
    )