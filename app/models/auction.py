#!/usr/bin/env python3

"""
Auction Table - Will contain all the Auction data
"""

from sqlalchemy import Column, Integer, VARCHAR, Float, ForeignKey, DateTime
from app.db.db import Base
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from typing import Optional


class Auction(Base):
    __tablename__ = "auctions"

    AuctionID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    CardID = Column(Integer, ForeignKey("cards.CardID", ondelete="CASCADE"), nullable=False)
    CardName = Column(VARCHAR, nullable=False)
    SellerID = Column(Integer, ForeignKey("cards.OwnerID", ondelete="CASCADE"), nullable=False)
    MinimumIncrement = Column(Float, nullable=False, default=0.01)
    Status = Column(VARCHAR, nullable=False, default="In Progress")
    EndTime = Column(DateTime, nullable=False)
    HighestBidderID = Column(Integer, nullable=False)
    HighestBid = Column(Float, nullable=False)
    ImageURL = Column(VARCHAR, nullable=False)
    
    # Relationship with Notifications, Cards and Sellers
    notifications = relationship('Notification', back_populates='auction', cascade="all, delete-orphan")
    card_id = relationship("Card", foreign_keys=[CardID], back_populates="card_id_auctions")
    seller_id = relationship("Card", foreign_keys=[SellerID], back_populates="seller_id_auction")

    def has_ended(self):
        """Check if the auction has ended."""
        return datetime.now(timezone.utc) > self.EndTime


class AuctionBase(BaseModel):
    AuctionID: Optional[int] = None  # Auto-incremented by the database
    CardID: Optional[int] = None     # Auto-incremented by the database
    CardName: str = Field(..., min_length=3, max_length=100, description="Card name must be between 3 to 100 characters.")
    MinimumIncrement: float = Field(..., gt=0, description="The minimum increment should be greater than 0.")
    EndTime: datetime = Field(..., description="End time must be a valid datetime.")
    Status: str
    HighestBidderID: int
    HighestBid: float
    ImageURL: str

    @field_validator("EndTime")
    @classmethod
    def check_endtime(cls, value : datetime):
        # Make sure end time is later than now
        if value <= datetime.now():
            raise ValueError("End Time must be later than today!")
        
        return value

class AuctionInfo(AuctionBase):
    pass

class AuctionBid(BaseModel):
    AuctionID: int
    BidAmount: float

class AuctionResponse(AuctionBase):
    AuctionID: int
    CardID: int
    SellerID: int
    MinimumIncrement: float
    
