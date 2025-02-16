from fastapi import FastAPI, Depends, HTTPException, File, Form, UploadFile, Query
from fastapi.responses import HTMLResponse
from app.services.auction_service import AuctionService
from app.services.profile_service import ProfileService
from sqlalchemy.orm import Session
from app.models.auction import Auction, AuctionInfo
from app.models.card import Card
from app.db.db import SessionLocal
from pydantic import BaseModel
from app.models.auction import AuctionInfo
from typing import Dict
import os
import shutil
import requests
import boto3
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

# Load .env file from a specific path
dotenv_path = os.path.join(os.path.dirname(__file__), "..","..", "aws_cognito.env")

# Load environment variables from .env file
load_dotenv(dotenv_path)

app = FastAPI()

# Read variables
COGNITO_REGION = os.getenv("COGNITO_REGION")
USER_POOL_ID = os.getenv("USER_POOL_ID")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")

# Cognito Issuer (used for token verification)
COGNITO_ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}"

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fetch Cognito public keys
def get_cognito_public_keys():
    """Fetch AWS Cognito's public keys to verify JWT tokens."""
    response = requests.get(f"{COGNITO_ISSUER}/.well-known/jwks.json")
    return response.json()["keys"]

COGNITO_PUBLIC_KEYS = get_cognito_public_keys()

# Verify Cognito JWT Token
def verify_cognito_token(token: str = Depends(oauth2_scheme)):
    """Verify JWT token from Cognito and extract user details."""
    try:
        header = jwt.get_unverified_header(token)
        key = next((key for key in COGNITO_PUBLIC_KEYS if key["kid"] == header["kid"]), None)
        if not key:
            raise HTTPException(status_code=403, detail="Invalid token")
        
        decoded_token = jwt.decode(token, key, algorithms=["RS256"], audience=COGNITO_CLIENT_ID, issuer=COGNITO_ISSUER)
        return {
            "username": decoded_token.get("cognito:username"),
            "email": decoded_token.get("email"),
        }
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Invalid token: {str(e)}")
# Dummy function to get logged-in user (replace with actual authentication)
def get_current_username():
    user_info = verify_cognito_token()
    username = user_info["username"]
    return username

@app.get("/auction-collection")
async def display_auction_page( page: int = Query(1, description="Page number"),  db: Session = Depends(get_db)):
    auctions = AuctionService.get_auctions_by_page(page)
    total_pages =  AuctionService.get_total_page()
    return {"auctions": auctions, "total_pages": total_pages}

@app.post("/auction-details/{auction_id}")
async def display_auction_details(auction_id:int, db: Session = Depends(get_db)):
    auction = AuctionService.auction_indiv(auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    return auction

@app.post("'/place-bid/{auction_id}")
async def place_bid(auction_id:int, bid_info: AuctionInfo, db: Session = Depends(get_db),current_user: dict = Depends(verify_cognito_token)):  # ✅ Require authentication
    auction_service = AuctionService(db)
    useremail = current_user.get("email")
    user_id = ProfileService.get_profile_id(useremail)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    return auction_service.bid_auction(auction_id, user_id, bid_info)
