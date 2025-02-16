from fastapi import Depends
from app.services.auction_service import AuctionService
from app.dependencies.db import get_db
from sqlalchemy.orm import Session

def get_auction_service(db: Session = Depends(get_db)) -> AuctionService:
    return AuctionService(db)