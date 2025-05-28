from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List  # List mejora la documentacion de la API

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


class Game(BaseModel):
    id: Optional[int]
    title: str
    category: str
    year: int


@app.get("/", tags=["Home"])
def home():
    return "Prueba FastAPI"


movies = [
    {
        "id": 1,
        "title": "Doctor Strange en el Multiverso de la Locura",
        "category": "Superhéroes",
        "year": 2023,
    },
    {
        "id": 2,
        "title": "Gato con Botas 2: El Último Deseo",
        "category": "Animada",
        "year": 2024,
    },
    {
        "id": 3,
        "title": "Lilo y Stitch",
        "category": "Live Action",
        "year": 2025,
    },
]

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
            return movie


# parametros query


@app.get("/movies/", tags=["Movies"])
def get_movie_by_category(category: str, year: int):
    for movie in movies:
        if movie["category"] == category:
            return movie


# metodo POST


@app.post("/movies", tags=["Movies"])
def create_movie(movie: Movie) -> List[Movie]:
    movies.append(movie.model_dump())  # convertir a diccionario
    return movies  # solo para observar las nuevas


# metodo PUT


@app.put("/movies/{id}", tags=["Movies"])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["category"] = movie.category
            item["year"] = movie.year
    return movies


# metodo DELETE


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
    return movies

