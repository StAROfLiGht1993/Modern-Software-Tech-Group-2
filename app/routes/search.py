from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.services.search_service import SearchService

router = APIRouter()

@router.get("/search/cards")
def search_cards(search_query: str, db: Session = Depends(get_db)):
    """
    Endpoint to search for cards based on the search query.
    """
    search_service = SearchService(db)
    return search_service.search_cards(search_query)

@router.get("/search/profiles")
def search_profiles(search_query: str, db: Session = Depends(get_db)):
    """
    Endpoint to search for profiles based on the search query.
    """
    search_service = SearchService(db)
    return search_service.search_profiles(search_query)