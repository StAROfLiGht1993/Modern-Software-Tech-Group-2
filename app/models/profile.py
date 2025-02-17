#!/usr/bin/env python3

"""
Profile Table - Will contain all the profile data
"""

from sqlalchemy import Column, Integer, VARCHAR
from app.db.db import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import relationship
from typing import Optional


class Profile(Base):
    __tablename__ = "profiles"

    UserID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Username = Column(VARCHAR, nullable=False, unique=True)
    Password = Column(VARCHAR, nullable=False)
    Email = Column(VARCHAR, nullable=True)  # PDPA # Shouldn't email be primary key now that authentication uses email as username, only one account per email
    NumberOfRating = Column(Integer, nullable=False, default=0)
    CurrentRating = Column(Integer, nullable=False, default=0)
    PhoneNumber = Column(Integer, nullable=True, default=0)
    CognitoUserID = Column(VARCHAR, nullable=True, unique=True)

    # Relationship with Cards and Notifications
    cards = relationship("Card", back_populates="profiles", cascade="all, delete-orphan")
    notifications = relationship('Notification', back_populates='user', cascade="all, delete-orphan")


class ProfileBase(BaseModel):
    UserID: Optional[int] = None # Auto-incremented by the database
    Username: str
    Password: str
    Email: str
    NumberofRating: Optional[int] = 0 
    CurrentRating: Optional[int] = 0.0
    PhoneNumber: Optional[int] = 0
    CognitoUserID: str


class ProfileInfo(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)
