import os
from typing import Any
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("singles_tennis_ranking")

# Constants
load_dotenv()
API_KEY = os.getenv('RAPID_API_KEY')
API_HOST = os.getenv('RAPID_API_HOST')

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST,
    "Content-Type": "application/json",
}

@mcp.tool()
@mcp.tool()
def get_singles_rankings(tour: str = "wta", limit: int = 5) -> list[dict[str, Any]]:
    try:
        response = httpx.get(f"https://{API_HOST}/tennis/v2/{tour}/ranking/singles/", headers=headers)
        
        if response.status_code == 429:
            return {
                "success": False,
                "error_code": 429,
                "message": "API rate limit exceeded."
            }

        if response.status_code != 200:
            return [{"error": f"HTTP Error: {response.status_code}"}]
    except httpx.TimeoutException:
        return [{"error": "The request timed out. Please try again."}]
    except httpx.RequestError:
        return [{"error": "Could not connect to the Tennis API."}]

    data = response.json()["data"]

    if not data:
        return [{"message": "No rankings found."}]

    rankings = []
    for player in data[:limit]:
        rankings.append({
            "position": player["position"],
            "id": player["player"]["id"],
            "name": player["player"]["name"],
            "country": player["player"]["countryAcr"],
            "ranking_points": player["rankingPoints"],
        })

    return rankings

@mcp.tool()
def get_head_to_head(tour: str = "atp", player1_id: int = 5136, player2_id: int = 47566) -> dict[str, Any]:
    if limit < 1:
        return {"error": "limit must be at least 1"}

    try:
        response = httpx.get(f"https://{API_HOST}/tennis/v2/{tour}/fixtures/h2h/{player1_id}/{player2_id}", headers=headers)
        if response.status_code == 429:
            return {
                "success": False,
                "error_code": 429,
                "message": "API rate limit exceeded."
            }

        if response.status_code != 200:
            return {"error": f"HTTP Error: {response.status_code}"}
    except httpx.TimeoutException:
        return [{"error": "The request timed out. Please try again."}]
    except httpx.RequestError:
        return [{"error": "Could not connect to the Tennis API."}]

    data = response.json()["data"]

    if not data:
        return {"message": "No head-to-head history found."}

    return {
        "player1_id": player1_id,
        "player2_id": player2_id,
        "fixtures": data,
    }

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()