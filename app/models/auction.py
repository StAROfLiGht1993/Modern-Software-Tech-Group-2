#!/usr/bin/env python3

"""
Auction Table - Will contain all the Auction data
"""

from sqlalchemy import Column, Integer, VARCHAR, Float, ForeignKey, DateTime
from app.db.db import Base
from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy.orm import relationship
from datetime import datetime


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
    EndTime : datetime
    HighestBidderID : int
    HighestBid : float

    @field_validator("EndTime")
    @classmethod
    def check_endtime(cls, value : datetime):
        # Make sure end time is later than now
        if value <= datetime.now():
            raise ValueError("End Time must be later than today!")
        
        return value

class AuctionInfo(AuctionBase):
    pass

class AuctionResponse(AuctionBase):
    model_config = ConfigDict(from_attributes=True)
    AuctionID: int
    CardID: int
    SellerID: int
    MinimumIncrement: float