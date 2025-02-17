#!/usr/bin/env python3

"""
Profile Table - Will contain all the profile data
"""

from sqlalchemy import Column, Integer, VARCHAR, Float
from app.db.db import Base
from pydantic import BaseModel, ConfigDict, field_validator
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

    # Relationship with Cards
    cards = relationship("Card", back_populates="profiles", cascade="all, delete-orphan")


class ProfileBase(BaseModel):
    UserID: Optional[int] = None # Auto-incremented by the database
    Username: str
    Password: str
    Email: str
    NumberofRating: Optional[int] = 0 
    CurrentRating: Optional[int] = 0.0
    PhoneNumber: Optional[int] = 0
    CognitoUserID: str

    @field_validator("Email")
    @classmethod
    def check_email(cls, value : str):
        # Check if the email contails @
        if len(value.split("@")) != 2:
            raise ValueError("Invalid Email!")
        
        return value
    
    @field_validator("PhoneNumber")
    @classmethod
    def check_phone_number(cls, value : int):
        # Check if phone number is 8 digits
        if (10000000 <= value <= 99999999):
            raise ValueError("Number must be 8 digits")
        # Check if phone number starts with 8 / 9
        if str(value)[0] not in {"8", "9"}:  # Check first digit
            raise ValueError("Number must start with 8 or 9")
        
        return value

class ProfileInfo(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)
