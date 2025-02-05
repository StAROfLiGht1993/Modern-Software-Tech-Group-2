#!/usr/bin/env python3

from sqlalchemy import Column, String, Float, Integer
from database import Base

class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    description = Column(String)
    starting_bid = Column(Float)
    minimum_increment = Column(Float)
    auction_duration = Column(Integer)
