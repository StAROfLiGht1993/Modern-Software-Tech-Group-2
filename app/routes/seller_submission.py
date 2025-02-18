#!/usr/bin/env python3

from fastapi import APIRouter, Form, File, UploadFile, HTTPException, status, Depends
from app.models.auction import Auction, AuctionResponse, AuctionInfo
from app.models.card import Card
from app.services.auction_service import AuctionService
from app.dependencies.services import get_auction_service
from app.dependencies.auth import req_user_role
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
import shutil
import os
import uuid
import logging
from sqlalchemy.orm import Session
from app.db.db import get_db
from pydantic import ValidationError

router = APIRouter()

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

'''To handle file uploads and form form data.'''
@router.post("/submit-auction", response_model=AuctionResponse, status_code=status.HTTP_201_CREATED) 
            #  dependencies=[Depends(req_user_role)])
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
        
    '''Generate a unique filename using UUID to ensure no conflict in filenames'''
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(IMAGE_DIR, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logging.debug(f"File saved successfully to: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save file: {str(e)}")
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

    # Validate the end time
    if end_time <= datetime.now():
        raise HTTPException(status_code=400, detail="End Time must be later than the current time!")

    # Validate the starting bid
    if starting_bid <= 0:
        raise HTTPException(status_code=400, detail="Starting bid must be greater than zero!")

    # Validate the minimum increment
    if minimum_increment <= 0:
        raise HTTPException(status_code=400, detail="Minimum increment must be greater than zero!")

    '''Create auction record'''
    auction_data = Auction(
        CardID=card.CardID,
        CardName=card_name,
        SellerID=card.OwnerID,
        MinimumIncrement=minimum_increment,
        EndTime=end_time,
        Status="In Progress", # Dummy status for now
        HighestBidderID=2, # Dummy bidder ID for now
        HighestBid=starting_bid, # Dummy starting bid for now. Should replace when the auction page comes in.
        ImageURL=f"{file_path}"
    )

    db.add(auction_data)
    db.commit()
    db.refresh(auction_data)
    
    try:
        return {
            "AuctionID": auction_data.AuctionID,
            "CardID": auction_data.CardID,
            "CardName": auction_data.CardName,
            "SellerID": auction_data.SellerID,
            "MinimumIncrement": auction_data.MinimumIncrement,
            "EndTime": auction_data.EndTime,
            "Status": auction_data.Status,
            "HighestBidderID": auction_data.HighestBidderID,
            "HighestBid": auction_data.HighestBid,
            "ImageURL": auction_data.ImageURL
        }
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Response validation error: {e.errors()}")