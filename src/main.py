from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List  # List mejora la documentacion de la API

#routers
from src.routers.movie_router import movie_router
from src.routers.game_router import game_router


app = FastAPI()

app.title = "Prueba FastApiBoost"

#home
@app.get("/", tags=["Home"], status_code=500, response_description="Esto debe devolver un error") # codigo de estado esperado, por defecto en 200, 500 es un error
def home():
    return PlainTextResponse(content="home", status_code=200) # Codigo de estado

#incluir routers
app.include_router(prefix="/movies", router=movie_router)
app.include_router(prefix="/games", router=game_router)

