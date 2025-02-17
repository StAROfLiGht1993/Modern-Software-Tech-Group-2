#!/usr/bin/env python3
"""
Basic Card CRUD Applications
"""

from fastapi import APIRouter, UploadFile, File, Depends, status, HTTPException
import os
import shutil
from models.card import CardResponse, CardInfo
from app.dependencies.auth import req_user_role, req_admin_role
from services.card_service import CardService
from app.dependencies.services import get_card_service

router = APIRouter()

@router.post("/{username}/cards",
             response_model=CardResponse,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(req_user_role), Depends(req_admin_role)])
async def add_card(
    username : str,
    review: CardInfo,
    service: CardService = Depends(get_card_service),
):
    """
    Route to add the card
    """
    # Check username has an ID
    new_card = service.add_card(username, review)
    if not new_card:
        raise HTTPException(status_code=404, detail=f"Username {username} does not exist, cannot add card")

    # TODO verify the card before uploading
    
    return new_card

@router.post("/{username}/cards/{card_id}",
             response_model=CardResponse,
             dependencies=[Depends(req_user_role), Depends(req_admin_role)])
async def delete_card(
    username : str,
    card_id : int,
    service : CardService = Depends(get_card_service),
):
    """
    Route to delete card
    """
    success = service.delete_card(card_id, username)
    if success == 401:
        raise HTTPException(status_code=401, detail=f"User not logged in")
    elif success == 403:
        raise HTTPException(status_code=403, detail=f"Card ID {card_id} does not belong to user, cannot delete")
    elif success == 404:
        raise HTTPException(status_code=404, detail=f"Card ID {card_id} not available")
    
    return {"message" : f"Card ID {card_id} belonging to user {username} deleted sucessfully"}

@router.post("/{username}/cards/all_cards",
             response_model=CardResponse)
async def read_card(
    username : str,
    service : CardService = Depends(get_card_service),
):
    """
    Route to read the cards owned by user
    """
    owned_cards = service.get_cards_by_username(username)
    if not owned_cards:
        raise HTTPException(status_code=404, detail=f"User {username} does not exist!")
    
    return owned_cards
