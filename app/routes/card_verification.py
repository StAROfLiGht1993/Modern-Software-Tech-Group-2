from fastapi import APIRouter, UploadFile, File
import os
import shutil
from app.services.card_verification import authenticate_card

router = APIRouter()

UPLOAD_DIR = "static/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload directory exists

@router.post("/verify-card")
async def verify_card(image: UploadFile = File(...)):
    """
    Uploads an image and checks if the Pokémon card is authentic using AI.
    """
    file_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Run AI-based verification
    verification_result = authenticate_card(file_path)

    return {
        "message": "Verification complete",
        "result": verification_result
    }
