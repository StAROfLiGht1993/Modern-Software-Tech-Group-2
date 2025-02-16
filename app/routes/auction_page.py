from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from app.services.auction_service import get_auctions_by_page, bid_auction, get_total_page
from app.db.db import SessionLocal
from pydantic import BaseModel
from app.models.auction import AuctionInfo
from typing import Dict

app = FastAPI()
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dummy function to get logged-in user (replace with actual authentication)
def get_current_user():
    return {"user_id": 456}  # This should come from authentication middleware

@app.get("/auction-collection")
async def display_auction_page(page):
    auctions = get_auctions_by_page(page)
    total_pages =  get_total_page()
    return {"auctions": auctions, "total_pages": total_pages}

@app.post("'/place-bid/{auction_id}")
async def place_bid(auction_id:int, bid_info: AuctionInfo, user : Dict = Depends(get_current_user)):
    user_id = user["user_id"]
    if user_id:
        return bid_auction(auction_id, user_id, bid_info)
