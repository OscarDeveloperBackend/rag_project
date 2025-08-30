from fastapi import APIRouter, UploadFile, File,Query
from app.controllers import pdf_controller

router = APIRouter()

@router.post("/upload")
def upload_pdf(file: UploadFile = File(...), clear: bool = Query(True)):
    return pdf_controller.handle_upload(file, clear=clear)
