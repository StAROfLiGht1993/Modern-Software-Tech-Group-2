#!/usr/bin/env python3

"""
Notification Table - Will contain all the notification data
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from app.db.db import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Notification(Base):
    __tablename__ = 'notifications'
    
    NotificationID = Column(Integer, primary_key=True, autoincrement=True)
    BidderID = Column(Integer, ForeignKey('profiles.UserID'), nullable=False)  # Link to the Profile (user)
    AuctionID = Column(Integer, ForeignKey('auctions.AuctionID'), nullable=False)  # Link to Auction
    Message = Column(String, nullable=False)
    TimeSent = Column(DateTime, nullable=False, default=datetime)  # Timestamp for the notification

    # Relationships to Profile and Auction
    user = relationship('Profile', back_populates='notifications')
    auction = relationship('Auction', back_populates='notifications')

    def __repr__(self):
        return f"<Notification(id={self.NotificationID}, user_id={self.BidderID}, auction_id={self.AuctionID}, message='{self.Message}', timestamp='{self.TimeSent}')>"
