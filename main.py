from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List  # List mejora la documentacion de la API
import datetime


app = FastAPI()

app.title = "Prueba FastApiBoost"

# modelos


class Movie(BaseModel):
    id: Optional[int]
    title: str
    category: str
    year: int


class MovieUpdate(BaseModel):
    title: str
    category: str
    year: int

class MovieCreate(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=15, default="My movie") #validaciones de datos
    category: str = Field(default="My category")
    year: int = Field(le=datetime.date.today().year, ge= 1900, default=0)

class GameCreate(BaseModel):
    id: int
    title: str
    category: str
    year: int

    model_config = {
        "json_schema_extra":{
            "example":{
                "id": 1,
                "title": "my game",
                "category": "my category",
                "year": 2025,
            }
        }
    }
    # validaciones mediante model_config

#gt greater than
#ge greater than or equal
#lt less than
#le less than or equal

class Game(BaseModel):
    id: Optional[int]
    title: str
    category: str
    year: int


@app.get("/", tags=["Home"])
def home():
    return "Prueba FastAPI"


movies : List[Movie] = []

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


# prueba endpoint


@app.get("/movies", tags=["Movies"])
def get_movies() -> List[Movie]:
    return movies

#prueba get con otra clase
@app.get("/games", tags=["Games"])
def get_games() -> List[Game]:
    return games


@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            return movie.model_dump

# parametros query


@app.get("/movies/", tags=["Movies"])
def get_movie_by_category(category: str, year: int):
    for movie in movies:
        if movie["category"] == category:
            return movie.model_dump
    return []

# metodo POST


@app.post("/movies", tags=["Movies"])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)  # convertir a diccionario
    return [movie.model_dump() for movie in movies]  # solo para observar las nuevas


@app.post("/games", tags=["Games"])
def create_game(game: GameCreate) -> List[Game]:
    games.append(game.model_dump())
    return games

# metodo PUT


@app.put("/movies/{id}", tags=["Movies"])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["category"] = movie.category
            item["year"] = movie.year
    return [movie.model_dump() for movie in movies]


# metodo DELETE


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    return [movie.model_dump() for movie in movies]