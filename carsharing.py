import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from db import engine
from routers import cars, web, auth
from routers.cars import BadTripException

# import db_array
# from schemas import Car, CarInput, CarOutput, TripInput, TripOutput, Trip

app = FastAPI(title="Car Sharing") # app = Rest service
app.include_router(web.router)
app.include_router(cars.router)
app.include_router(auth.router)

# permitir el acceso a la api desde otro dominio
origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# inicia antes de cualquier request del cliente
@app.on_event("startup") # no se puede mover a otro file xq necesita 'app' object
def on_startup():
  SQLModel.metadata.create_all(engine) # cheque si la db existe, sino la crea


@app.exception_handler(BadTripException)
async def unicorn_exception_handler(request: Request, exc: BadTripException):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Bad Trip"},
    )

# se comento para probar el test de home
# @app.middleware("http")
# async def add_cars_cookie(request: Request, call_next):
#     response = await call_next(request)
#     response.set_cookie(key="cars_cookie", value="you_visited_the_carsharing_app")
#     return response


# permite correr el programa solo con el boton de play
if __name__ == "__main__":
  uvicorn.run("carsharing:app", reload=True)






# db_array = db_array.db
# db = load_db()
  
# @app.get("/api/cars")
# def get_cars():
#   return db_array;


# buscando por el size del car y cantidad de puertas
# query parametros son pasados en la url despues de '?' y sepadaros por '&'
# @app.get("/api/cars")
# def get_cars(size: str|None = None, doors: int|None = None) -> list: # tipo de retorno es una lista
#   result = db_array
#   if size:
#     result = [car for car in result if car['size'] == size];
#   if doors:
#     result = [car for car in result if car['doors'] >= doors]
#   else: 
#     return result
  
  
# # usando la db en formato json
# @app.get("/api/cars")
# def get_cars(size: str|None = None, doors: int|None = None) -> list: # tipo de retorno es una lista
#   result = db
#   if size:
#     result = [car for car in result if car.id == size];
#   if doors:
#     result = [car for car in result if car.doors >= doors]
#   else: 
#     return result
  
