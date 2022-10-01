import uvicorn

from sqlmodel import  SQLModel

from fastapi import FastAPI

from db import engine
from routers import cars, web

# import db_array
# from schemas import Car, CarInput, CarOutput, TripInput, TripOutput, Trip

app = FastAPI(title="Car Sharing") # app = Rest service
app.include_router(web.router)
app.include_router(cars.router)


# inicia antes de cualquier request del cliente
@app.on_event("startup") # no se puede mover a otro file xq necesita 'app' object
def on_startup():
  SQLModel.metadata.create_all(engine) # cheque si la db existe, sino la crea



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
  
