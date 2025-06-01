from fastapi import FastAPI, Body, Path, Query, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse, Response
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Annotated  # List mejora la documentacion de la API
from src.utils.http_error_handler import HTTPErrorHandler

#routers
from src.routers.movie_router import movie_router
from src.routers.game_router import game_router

#motores de plantillas
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

#dependencias globales
# def dependency1 (param1: str):
#     print("dependencia global1")

# app = FastAPI(dependencies=dependency1)

app = FastAPI()

#middleware
app.add_middleware(HTTPErrorHandler)

#middleware de fastAPI
# @app.middleware('http')
# async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
#     print ('middleware is running!')
#     return await call_next(request)

#plantilla
static_path = os.path.join(os.path.dirname(__file__),"static/")
templates_path = os.path.join(os.path.dirname(__file__),"templates")

app.mount("/static", StaticFiles(directory=static_path), "static")
templates = Jinja2Templates(directory=templates_path)


app.title = "Prueba FastApiBoost"

#home
@app.get("/", tags=["Home"], status_code=500, response_description="Esto debe devolver un error") # codigo de estado esperado, por defecto en 200, 500 es un error
def home(request: Request):
    #return PlainTextResponse(content="home", status_code=200) # Codigo de estado
    return templates.TemplateResponse('index.html', {'request':request,'message':'Welcome'})

#incluir routers
app.include_router(prefix="/movies", router=movie_router)
app.include_router(prefix="/games", router=game_router)



# injeccion de dependecias

# tambien mediante clases

# class commonDep:
#     def __init__(self, start_date: str, end_date: str) -> None:
#         self.start_date = start_date
#         self.end_date = end_date
# al usar como clase se tienen que cambiar la forma de llamarlos de commons['start_date'] a commons.start_date


def common_params(start_date: str, end_date: str):
    return {"start_date":start_date, "end_date":end_date}

commonsDep = Annotated[dict, Depends(common_params)]

@app.get("/user", tags=["dependencies"])
def get_users(commons: commonsDep):
    return f"user init betwen {commons['start_date']} and {commons['end_date']}"

@app.get("/costumer", tags=["dependencies"])
def get_costumers(commons: commonsDep):
    return f"costumer init betwen {commons['start_date']} and {commons['end_date']}"