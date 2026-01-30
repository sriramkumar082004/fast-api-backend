from typing import Annotated
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Response
from app.services import ocr, bg_removal
from app.core import deps
from app.models.user import User

router = APIRouter()


@router.post("/ocr")
async def extract_aadhaar_data(
    file: UploadFile = File(...),
    # Optional: Protect this endpoint
    # current_user: User = Depends(deps.get_current_user)
):
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()
    result = ocr.extract_aadhaar_info(contents)
    return result


@router.post("/remove-bg")
async def remove_background_image(
    file: UploadFile = File(...),
    # Optional: Protect this endpoint
    # current_user: User = Depends(deps.get_current_user)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()
    try:
        processed_image = await bg_removal.remove_background(contents, file.filename)
        return Response(content=processed_image, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
