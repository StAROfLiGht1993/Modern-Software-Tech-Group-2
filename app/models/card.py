#!/usr/bin/env python3

"""
Card Table - Will contain all the card data
"""

from sqlalchemy import Column, Integer, VARCHAR, String, Boolean, ForeignKey
from app.db.db import Base
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import relationship


class Card(Base):
    __tablename__ = "cards"
    CardID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    OwnerID = Column(
        Integer, ForeignKey("profiles.UserID", ondelete="CASCADE"), nullable=False
    )

    CardQuality = Column(String, nullable=False, default="UNDEFINED")
    CardName = Column(VARCHAR, nullable=False)
    IsValidated = Column(Boolean, nullable=False, default=False)

    profiles = relationship("Profile", back_populates="cards")
    card_id_auctions = relationship("Auction", back_populates="card_id", foreign_keys="[Auction.CardID]") # Reference the card ID
    seller_id_auction = relationship("Auction", back_populates="seller_id", foreign_keys="[Auction.SellerID]") # Reference to the seller


class CardBase(BaseModel):
    CardQuality: str = Field(..., min_length=3, max_length=10, description="Card quality must be between 3 to 10 characters.")
    CardName: str = Field(..., min_length=3, max_length=100, description="Card name must be between 3 to 100 characters.")
    IsValidated: bool


class CardInfo(CardBase):
    pass


class CardResponse(CardBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    book_id: int
