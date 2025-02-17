#!/usr/bin/env python3

"""
Card DB Services, run database queries for specific manipulations
"""

from sqlalchemy.orm import Session
from app.models.card import Card, CardInfo
from app.models.profile import Profile


class CardService:
    def __init__(self, db: Session):
        self.db = db

    def get_cards_by_username(self, username: str):
        """
        Get all the cards that are owned by a username
        """
        # Check if the username exists
        profile = self.db.query(Profile).filter(Profile.Username == username).first()
        if not profile:
            return None
        user_id = profile.UserID

        return self.db.query(Card).filter(Card.OwnerID == user_id).all()

    def add_card(self, username: str, card_data: CardInfo):
        """
        Specific User adds new card
        """
        # Check if the user_id exist
        profile = self.db.query(Profile).filter(Profile.Username == username).first()
        if not profile:
            return None
        user_id = profile.UserID
        new_card = Card(OwnerID=user_id, **card_data.model_dump())
        self.db.add(new_card)
        self.db.commit()
        self.db.refresh(new_card)
        return new_card

    def delete_card(self, card_id: int, username: str):
        """
        Delete card for specific User
        """
        # Check if the card exists
        profile = self.db.query(Profile).filter(Profile.Username == username).first()
        if not profile:
            # TODO Return a forbidden permissons error here
            return 401
        card = self.db.query(Card).filter(
            Card.CardID == card_id, Card.OwnerID == profile.UserID
        )
        card_exists = self.db.query(Card).filter(
            Card.CardID == card_id
        )
        if not card:
            # Unauthorized
            return 403
        if not card_exists:
            # Card does not exist
            return 404
        self.db.delete(card)
        self.db.commit()
        return True
