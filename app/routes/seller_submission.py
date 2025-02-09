#!/usr/bin/env python3

from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uvicorn

router = APIRouter()

# Get the base directory where seller_submission.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct directories based on new folder structure
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(
    BASE_DIR, "templates"
)  # Now correctly points to Seller Submission/templates
IMAGE_DIR = os.path.join(STATIC_DIR, "images")

# Ensure directories exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# Mount static files
# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@router.post("/submit-auction")
async def create_auction(
    file: UploadFile = File(...),
    description: str = Form(...),
    starting_bid: float = Form(...),
    minimum_increment: float = Form(...),
    auction_duration: float = Form(...),  # Change to float to allow fractional hours
):
    """Handles auction submission and saves the uploaded image."""

    # Ensure minimum increment is at least 0.01
    if minimum_increment < 0.01:
        raise HTTPException(
            status_code=400, detail="Minimum increment must be at least 0.01"
        )

    # Ensure auction duration is valid (e.g., > 0 hours)
    if auction_duration <= 0:
        raise HTTPException(
            status_code=400, detail="Auction duration must be greater than 0 hours"
        )

    # Define file path
    file_path = os.path.join(IMAGE_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    return {
        "filename": file.filename,
        "file_url": f"/static/images/{file.filename}",
        "description": description,
        "starting_bid": starting_bid,
        "minimum_increment": minimum_increment,
        "auction_duration": auction_duration,  # Now in hours
    }


@router.get("/sell")
def get_form():
    """Serve the seller submission HTML page as a static file."""
    html_file_path = os.path.join(TEMPLATES_DIR, "seller_submission.html")

    # Debug print to verify file path
    print(f"DEBUG: Checking template file at: {html_file_path}")
    print(f"DEBUG: File exists? -> {os.path.exists(html_file_path)}")

    # Ensure the file exists before serving
    if not os.path.exists(html_file_path):
        raise HTTPException(status_code=404, detail="Template file not found!")

    return FileResponse(html_file_path, media_type="text/html")\
