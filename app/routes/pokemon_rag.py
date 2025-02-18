from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.pokemon_rag_service import PokemonRagService

router = APIRouter()
pokemon_service = PokemonRagService()

class PokemonQuery(BaseModel):
    pokemon_name: str

@router.post("/fetch", status_code=status.HTTP_200_OK)
async def fetch_pokemon(request: PokemonQuery):
    """
    ✅ Fetch Pokémon details from the Pokémon TCG API.
    """
    try:
        card_info = await pokemon_service.fetch_pokemon_details(request.pokemon_name)
        if "error" in card_info:
            raise HTTPException(status_code=404, detail=card_info["error"])
        return card_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
