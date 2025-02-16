#!/usr/bin/env python3

"""
Card Table - Will contain all the card data
"""

from sqlalchemy import Column, Integer, VARCHAR, String, Boolean, ForeignKey
from app.db.db import Base
from pydantic import BaseModel, ConfigDict
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
    auctions = relationship("Auction", back_populates="card") # We dont want to delete previous auctions


class CardBase(BaseModel):
    review: str


class CardInfo(CardBase):
    pass


class CardResponse(CardBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    book_id: int
