from fastapi import FastAPI, APIRouter, Form, File, UploadFile, HTTPException, Depends, status
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import uuid
from pathlib import Path
from decimal import Decimal
from app.services.auction_service import AuctionService
from app.models.auction import AuctionInfo, AuctionResponse
from app.dependencies.services import get_auction_service
import logging

app = FastAPI()
router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the base directory where the script is located
BASE_DIR = Path(__file__).resolve().parent.parent  
STATIC_DIR = BASE_DIR / "static"
IMAGE_DIR = STATIC_DIR / "images"  
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB limit

def generate_unique_filename(filename: str) -> str:
    """Generate a unique filename using UUID to prevent overwrites"""
    extension = Path(filename).suffix.lower()
    return f"{uuid.uuid4()}{extension}"

def is_valid_file(filename: str) -> bool:
    """Check if the file extension is allowed"""
    return Path(filename).suffix.lower().strip(".") in ALLOWED_EXTENSIONS

@router.post("/submit-auction", response_model=AuctionResponse, status_code=status.HTTP_201_CREATED)
def create_auction(
    file: UploadFile = File(...),
    card_id: int = Form(...),
    description: str = Form(...),
    starting_bid: Decimal = Form(...),
    minimum_increment: Decimal = Form(...),
    auction_duration: float = Form(...),
    service: AuctionService = Depends(get_auction_service),
):
    """Handles auction submission and saves the uploaded image."""

    # Validate auction parameters
    if starting_bid <= 0:
        raise HTTPException(status_code=400, detail="Minimum starting bid must be greater than $0")
    if minimum_increment < Decimal("0.01"):
        raise HTTPException(status_code=400, detail="Minimum increment must be at least 0.01")
    if auction_duration <= 0:
        raise HTTPException(status_code=400, detail="Auction duration must be greater than 0 hours")
    
    # Validate file type
    if not is_valid_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.")
        
    # Generate a unique file name
    unique_filename = generate_unique_filename(file.filename)
    file_path = IMAGE_DIR / unique_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"Failed to save file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Store auction details (via service layer)
    auction_info = AuctionInfo(
        card_id=card_id,
        description=description,
        starting_bid=starting_bid,
        minimum_increment=minimum_increment,
        auction_duration=auction_duration,
        image_url=f"/static/images/{unique_filename}"
    )
    
    try:
        created_auction = service.create_auction(auction_info)
    except Exception as e:
        logger.error(f"Failed to create auction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create auction: {str(e)}")

    if not created_auction:
        raise HTTPException(status_code=400, detail="Failed to create auction")

    return AuctionResponse(
        id=created_auction.id,
        card_id=created_auction.card_id,
        description=created_auction.description,
        starting_bid=created_auction.starting_bid,
        minimum_increment=created_auction.minimum_increment,
        auction_duration=created_auction.auction_duration,
        image_url=created_auction.image_url
    )

app.include_router(router)
