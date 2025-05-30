from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
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
    year: int = Field(le=datetime.date.today().year, ge= 1900, default=2000)

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


@app.get("/", tags=["Home"], status_code=500, response_description="Esto debe devolver un error") # codigo de estado esperado, por defecto en 200, 500 es un error
def home():
    return PlainTextResponse(content="home", status_code=200) # Codigo de estado


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


@app.get("/movies", tags=["Movies"], status_code=200, response_description="Este debe retornar una respuesta exitosa")
def get_movies() -> List[Movie]:
    content = movies
    return JSONResponse(content=content)

#prueba get con otra clase
@app.get("/games", tags=["Games"])
def get_games() -> List[Game]:
    return games


@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int = Path(ge=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return movie
    return {}

# parametros query


@app.get("/movies/", tags=["Movies"])
def get_movie_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    movies_category : List[Movie] = []
    for movie in movies:
        if movie.category == category:
            movies_category.append(movie)
    return movies_category

# metodo POST


@app.post("/movies", tags=["Movies"])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)  # convertir a diccionario
    content = [movie.model_dump() for movie in movies]  # solo para observar las nuevas
    return JSONResponse(content=content, status_code=200) 
    #return RedirectResponse("/movies", status_code=303) #prueba RedirectResponse


@app.post("/games", tags=["Games"])
def create_game(game: GameCreate) -> List[Game]:
    games.append(game.model_dump())
    return games

# metodo PUT


@app.put("/movies/{id}", tags=["Movies"])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.category = movie.category
            item.year = movie.year
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


# metodo DELETE


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


# FileResponse

@app.get("/get_file", tags=["Files"])
def get_files():
    return FileResponse("Dummy PDF.pdf")


# CODIGOS DE ESTADO

# 200	OK	Todo salió bien (GET, PUT exitoso)
# 201	Created	Recurso creado exitosamente (POST)
# 204	No Content	Acción exitosa pero sin contenido que devolver
# 400	Bad Request	Datos inválidos enviados por el cliente
# 401	Unauthorized	No autenticado
# 403	Forbidden	Autenticado pero no autorizado
# 404	Not Found	Recurso no encontrado
# 409	Conflict	Conflicto (por ejemplo, ya existe el recurso)
# 422	Unprocessable Entity	Validación fallida (automáticamente por FastAPI)
# 500	Internal Server Error	Error del servidor