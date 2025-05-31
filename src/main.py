from fastapi import FastAPI, Body, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse, Response
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List  # List mejora la documentacion de la API
from src.utils.http_error_handler import HTTPErrorHandler

#routers
from src.routers.movie_router import movie_router
from src.routers.game_router import game_router


app = FastAPI()

#middleware
app.add_middleware(HTTPErrorHandler)

#middleware de fastAPI
# @app.middleware('http')
# async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
#     print ('middleware is running!')
#     return await call_next(request)

app.title = "Prueba FastApiBoost"

#home
@app.get("/", tags=["Home"], status_code=500, response_description="Esto debe devolver un error") # codigo de estado esperado, por defecto en 200, 500 es un error
def home():
    return PlainTextResponse(content="home", status_code=200) # Codigo de estado

#incluir routers
app.include_router(prefix="/movies", router=movie_router)
app.include_router(prefix="/games", router=game_router)

