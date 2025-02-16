#!/usr/bin/env python3

"""
Auction Services, run database queries for specific manipulations
"""

from sqlalchemy.orm import Session
from app.models.card import Card, CardInfo
from app.models.profile import Profile
from app.models.auction import Auction, AuctionInfo
from profile_service import ProfileService
from datetime import datetime
from fastapi import HTTPException

from typing import Union


class AuctionService:
    def __init__(self, db: Session):
        self.db = db

    def get_auctions_by_page(self, page:int,page_size: int = 10):
        """
        Get auctions by page limited to 10 auctions per page
        Display the expiring auctions first
        """
        current_date = datetime.today().date() # assume endtime is a date
        offset = (page - 1) * page_size  # Pagination offset
        return (
            self.db.query(            
            Auction.AuctionID,
            Auction.CardID,
            Auction.title,
            Auction.Status,
            Auction.HighestBid,
            Card.IsValidated,
            Card.CardName,
            Card.CardQuality,
            Auction.ImageURL  # Ensure this is the correct field in `Card)
            )
        .join(Card, Auction.CardID == Card.CardID)  # Join auctions with card details
        .filter(Auction.EndTime >= current_date)  # Only include auctions that are not expired
        .order_by(Auction.EndTime)  # Sort by earliest expiration
        .offset(offset)
        .limit(page_size)
        .all()
    )

    def get_auctions_details(self, auction_id: int):
        """
        Get auctions by auction id for bidding
        """
        auction_indiv = ( 
            self.db.query(            
            Auction.AuctionID,
            Auction.CardID,
            Auction.title,
            Auction.Status,
            Auction.HighestBid,
            Card.IsValidated,
            Card.CardName,
            Card.CardQuality,
            Card.CardDescription,
            Auction.ImageURL  # Ensure this is the correct field in `Card)
            )
            .join(Card, Auction.CardID == Card.CardID)  # Join auctions with card details
            .filter(Auction.AuctionID == auction_id) 
            .first()
        )
        if not auction_indiv:
            raise HTTPException(status_code=404, detail="Auction not found")
        return auction_indiv



    def get_total_page(self):
            """
            Get total page of auctions
            """
            current_date = datetime.today().date() # assume endtime is a date
            available_auction = self.db.query(Auction).filter(Auction.EndTime>=current_date).all()
            return len(available_auction) // 10 + 1
    
    def get_auction_by_id(self, auction_id: int):
        """
        Get specific auction by auction ID
        """
        return self.db.query(Auction).filter(Auction.AuctionID == auction_id).first()

    def add_auction(self, card_id: int, auction_data: AuctionInfo):
        """
        Add a new Auction
        """
        # Check if Card Exists
        card = self.db.query(Card).filter(Card.CardID == card_id).first()
        if not card:
            return None
        new_auction = Auction(
            CardID=card.CardID, SellerID=card.OwnerID, **auction_data.model_dump()
        )
        self.db.add(new_auction)
        self.db.commit()
        self.db.refresh(new_auction)
        return new_auction

    def update_auction(self, auction_id: int, user_id: int, update_info: AuctionInfo):
        """
        Update the auction data
        """
        # Check if auction exists under user
        auction = self.get_auction_by_id(auction_id)
        if not auction:
            return None  # Auction does not exist
        auction = (
            self.db.query(Auction)
            .filter(Auction.AuctionID == auction_id, Auction.SellerID == user_id)
            .first()
        )
        if not auction:
            return None  # User does not have permission to edit auction
        for key, value in update_info.model_dump().items():
            setattr(auction, key, value)
        self.db.commit()
        self.db.refresh(auction)
        return auction

    def bid_auction(self, auction_id: int, user_id: int, bid_info: AuctionInfo):
        """
        Make a new bid in an auction
        """
        # Check if auction exists
        auction = self.get_auction_by_id(auction_id)
        if not auction:
            return None  # Auction Does not exist
        # # Check if user exists
        # bidder_profile = (
        #     self.db.query(Profile).filter(Profile.UserID == user_id).first()
        # )
        # if not bidder_profile:
        #     return None  # Return 404 profile not found

        # Check if current bid is higher than latest bid
        if auction.HighestBid >= bid_info.HighestBid:
            return None  # Current bid not high enough
        else:
            for key, value in bid_info.model_dump().items():
                setattr(auction, key, value)
            self.db.commit()
            self.db.refresh(auction)
            return auction

    def get_auction_by_card_name_qualty(
        self, card_name: str, card_quality: str = "None"
    ):
        """
        Retrieve auctions by specific card name
        """
        if card_quality == "None":
            cards = self.db.query(Card).filter(Card.CardName == card_name).all()
        else:
            cards = (
                self.db.query(Card)
                .filter(Card.CardName == card_name, Card.CardQuality == card_quality)
                .all()
            )

        # We then search the auctions by their specific card_ids to match
        auction_list = []
        for select_card in cards:
            auction_list.extend(
                self.db.query(Auction).filter(
                    Auction.CardID == select_card.CardID,
                    Auction.SellerID == select_card.OwnerID,
                )
            )

        return auction_list
