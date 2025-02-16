#!/usr/bin/env python3

from fastapi import APIRouter, Form, File, UploadFile, HTTPException, status, Depends
from app.models.auction import Auction, AuctionInfo, AuctionResponse
from app.models.card import Card
from app.services.auction_service import AuctionService
from app.dependencies.services import get_auction_service
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
import shutil
import os
import uuid
import logging
from sqlalchemy.orm import Session
from app.db.db import get_db

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the base directory one level up from where seller_submission.py is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Correct directories based on new folder structure
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
IMAGE_DIR = os.path.join(STATIC_DIR, "images")

# Ensure directories exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# Mount static files
# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

'''To handle file uploads and form form data.'''
@router.post("/submit-auction", response_model=AuctionResponse, status_code=status.HTTP_201_CREATED)
def create_auction(
    file: UploadFile = File(...),
    card_name: str = Form(...),
    card_quality: str = Form(...),
    is_validated: bool = Form(...),
    starting_bid: float = Form(...),
    minimum_increment: float = Form(...),
    auction_duration: float = Form(...),
    service: AuctionService = Depends(get_auction_service),
    db: Session = Depends(get_db)
):
    logger.debug("Received auction submission request")
    '''HTTPException - To handle auction submission'''
    # Ensure starting bid is greater than 0
    if starting_bid < 0:
        logger.error("Starting bid cannot be negative")
        raise HTTPException(status_code=400, detail="Starting bid cannot be negative.")
    
    # Ensure minimum increment is greater than 0
    if minimum_increment <= 0:
        logger.error("Minimum increment must be greater than 0")
        raise HTTPException(status_code=400, detail="Minimum increment must be greater than 0.")
    
    # Ensure that auction duration is greater than 0.
    if auction_duration <= 0:
        logger.error("Auction duration must be greater than 0")
        raise HTTPException(status_code=400, detail="Auction duration must be greater than 0.")
    
    '''Generate a unique filename using UUID'''
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(IMAGE_DIR, unique_filename)

    logger.debug(f"Saving file to: {file_path}")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.debug(f"File saved successfully to: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save file: {str(e)}")
        print("500 was raised")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    '''Create card record'''
    card = Card(CardName=card_name,
                CardQuality=card_quality,
                OwnerID=1, # Dummy owner ID for now
                IsValidated=is_validated)
    db.add(card)
    db.commit()
    db.refresh(card)

    '''Calculate the end time of the auction'''
    end_time = datetime.now() + timedelta(hours=auction_duration)

    '''Create auction record'''
    auction_data = AuctionInfo(
        CardID=card.CardID,
        CardName=card_name,
        MinimumIncrement=minimum_increment,
        EndTime=end_time,
        Status="In Progress", # Dummy status for now
        HighestBidderID=2, # Dummy bidder ID for now
        HighestBid=starting_bid, # Dummy starting bid for now. Should replace when the auction page comes in.
        ImageURL=f"{file_path}"
    )

    service.add_auction(auction_data)
    
    return {
        "AuctionID": auction_data.AuctionID,
        "CardID": auction_data.CardID,
        "SellerID": auction_data.SellerID,
        "MinimumIncrement": auction_data.MinimumIncrement,
        "EndTime": auction_data.EndTime,
        "Status": auction_data.Status,
        "HighestBidderID": auction_data.HighestBidderID,
        "HighestBid": auction_data.HighestBid,
        "ImageURL": auction_data.ImageURL
    }

