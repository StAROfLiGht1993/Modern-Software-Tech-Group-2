#!/usr/bin/env python3

"""
Auction Table - Will contain all the Auction data
"""

from sqlalchemy import Column, Integer, VARCHAR, Float, ForeignKey, DateTime
from app.db.db import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import relationship
from decimal import Decimal


class Auction(Base):
    __tablename__ = "auctions"

    AuctionID = Column(Integer, primary_key=True, index=True)
    CardID = Column(
        Integer, ForeignKey("cards.CardID", ondelete="CASCADE"), nullable=False
    )
    SellerID = Column(
        Integer, ForeignKey("cards.OwnerID", ondelete="CASCADE"), nullable=False
    )

    MinimumIncrement = Column(Float, nullable=False, default=0.01)
    Status = Column(VARCHAR, nullable=False, default="In Progress")
    EndTime = Column(DateTime, nullable=False)

    HighestBidderID = Column(Integer, nullable=False)
    HighestBid = Column(Float, nullable=False)

class AuctionBase(BaseModel):
    AuctionID : int
    CardID : int
    SellerID : int
    MinimumIncrement : float
    Status : str
    HighestBidderID : int
    HighestBid : float

class AuctionInfo(BaseModel):
    card_id: int
    description: str
    starting_bid: Decimal
    minimum_increment: Decimal
    auction_duration: float
    image_url: str

class AuctionResponse(BaseModel):
    id: int
    card_id: int
    description: str
    starting_bid: Decimal
    minimum_increment: Decimal
    auction_duration: float
    image_url: str