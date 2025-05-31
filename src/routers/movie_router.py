from fastapi import FastAPI, Body, Path, Query, APIRouter
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from src.models.movie_models import Movie, MovieCreate, MovieUpdate

movies : List[Movie] = []

# Router
movie_router = APIRouter()

# prueba endpoints

@movie_router.get("/", tags=["Movies"], status_code=200, response_description="Este debe retornar una respuesta exitosa")
def get_movies() -> List[Movie]:
    content = movies
    return JSONResponse(content=content)

@movie_router.get("/{id}", tags=["Movies"])
def get_movie(id: int = Path(ge=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return movie
    return {}

# parametros query


@movie_router.get("/by_category", tags=["Movies"])
def get_movie_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    movies_category : List[Movie] = []
    for movie in movies:
        if movie.category == category:
            movies_category.append(movie)
    return movies_category

# metodo POST


@movie_router.post("/", tags=["Movies"])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)  # convertir a diccionario
    content = [movie.model_dump() for movie in movies]  # solo para observar las nuevas
    return JSONResponse(content=content, status_code=200) 
    #return RedirectResponse("/movies", status_code=303) #prueba RedirectResponse

# metodo PUT


@movie_router.put("/{id}", tags=["Movies"])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.category = movie.category
            item.year = movie.year
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


# metodo DELETE


@movie_router.delete("/{id}", tags=["Movies"])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

# FileResponse

@movie_router.get("/get_file", tags=["Files"])
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