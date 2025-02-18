import os
import requests

class PokemonRagService:
    def __init__(self):
        self.pokemon_api_url = "https://api.pokemontcg.io/v2/cards"
        self.api_key = os.getenv("POKEMON_TCG_API_KEY")

    async def fetch_pokemon_details(self, pokemon_name: str):
        """
        ✅ Fetch Pokémon details from Pokémon TCG API.
        """
        headers = {"X-Api-Key": self.api_key} if self.api_key else {}

        url = f"{self.pokemon_api_url}?q=name:\"{pokemon_name}\"&pageSize=1"
        print(f"📡 API Request URL: {url}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # ✅ Ensure request is successful
            data = response.json()

            if "data" not in data or not data["data"]:
                return {"error": f"No Pokémon card found for '{pokemon_name}'."}

            card_data = data["data"][0]  # ✅ Take the first result
            print(f"✅ API Response: {card_data}")

            return {
                "name": card_data.get("name", "Unknown"),
                "set": card_data.get("set", {}).get("name", "Unknown"),
                "rarity": card_data.get("rarity", "Unknown"),
                "image_url": card_data.get("images", {}).get("large", "No Image Available")
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch data from Pokémon API: {str(e)}"}
