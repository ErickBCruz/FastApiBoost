from fastapi import FastAPI, Body, Path, Query, APIRouter
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from src.models.game_models import Game, GameCreate

games = [
    {
        "id": 1,
        "title": "Mario",
        "category": "rpg",
        "year": 1999,
    },
    {
        "id": 2,
        "title": "Donkey kong",
        "category": "plataformas",
        "year": 2000,
    },
    {
        "id": 3,
        "title": "Halo",
        "category": "Shooter",
        "year": 2010,
    },
]

#router
game_router = APIRouter()

#prueba get con otra clase
@game_router.get("/", tags=["Games"])
def get_games() -> List[Game]:
    return games

@game_router.post("/", tags=["Games"])
def create_game(game: GameCreate) -> List[Game]:
    games.append(game.model_dump())
    return games