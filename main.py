from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()

app.title = "Prueba FastApiBoost"


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


# prueba endpoint


@app.get("/movies", tags=["Movies"])
def get_movies():
    return movies


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
def create_movie(
    id: int = Body(), title: str = Body(), category: str = Body(), year: int = Body()
):
    movies.append(
        {
            "id": id,
            "title": title,
            "category": category,
            "year": year,
        }
    )
    return movies  # solo para observar las nuevas


# metodo PUT


@app.put("/movies/{id}", tags=["Movies"])
def update_movie(title: str = Body(),
                category: str = Body(),
                year: int = Body()):
    for movie in movies:
        if movie["title"] == title:
            movie["category"] = category
            movie["year"] = year
    return movies


# metodo DELETE

@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
    return movies