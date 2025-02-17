from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile, Query
from fastapi.responses import HTMLResponse, JSONResponse
from app.services.auction_service import AuctionService
from app.services.profile_service import ProfileService
from sqlalchemy.orm import Session
from app.models.auction import Auction, AuctionInfo, AuctionBid
from app.models.card import Card
from app.dependencies.services import get_auction_service, get_profile_service
from pydantic import BaseModel
from app.models.auction import AuctionInfo
from app.models.notifications import Notification
from typing import Dict
from sqlalchemy.orm import Session
import os
import shutil
import requests
import boto3
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

from app.routes.auth import cognito_service

router = APIRouter()

@router.get("/auction-collection")
async def display_auction_page( page: int = Query(1, description="Page number"),  auction_service: Session = Depends(get_auction_service)):
    auctions = auction_service.get_auctions_by_page(page)
    total_pages =  auction_service.get_total_page()
    print(auctions)
    print(total_pages)
    return {"auctions": auctions, "total_pages": total_pages}

@router.get("/auction-details/{auction_id}")
async def display_auction_details(auction_id:int, auction_service: AuctionService = Depends(get_auction_service)):
    auction = auction_service.get_auctions_details(auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    return auction

@router.post("/place-bid")
async def place_bid(bid_info: AuctionBid, auction_service: AuctionService = Depends(get_auction_service), profile_service: ProfileService = Depends(get_profile_service), auth_info: dict = Depends(cognito_service.validate_token)):  # ✅ Require authentication
    useremail = auth_info.get("username")
    user_id = profile_service.get_profile_id(useremail)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    auction = auction_service.bid_auction(user_id, bid_info)
    if auction:
        return auction
    else:
        raise HTTPException(status_code=400, detail="Failed to place bid")

@app.get("/notifications/{user_id}")
async def get_notifications(user_id: int, db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.BidderID == user_id).all()
    result = [{"auction_id": n.AuctionID, "message": n.Message, "timestamp": n.TimeSent.isoformat()} for n in notifications]
    return JSONResponse(content=result)