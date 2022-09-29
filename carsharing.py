import uvicorn

from fastapi import FastAPI, HTTPException

import db_array
from schemas import CarInput, CarOutput, load_db, save_db

db_array = db_array.db
db = load_db()

app = FastAPI() # app = Rest service

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
  
  
# usando la db en formato json
@app.get("/api/cars")
def get_cars(size: str|None = None, doors: int|None = None) -> list: # tipo de retorno es una lista
  result = db
  if size:
    result = [car for car in result if car.id == size];
  if doors:
    result = [car for car in result if car.doors >= doors]
  else: 
    return result

#al especificar el tipo de dato con 'type hints' python nos ayuda para saber que se debe enviar o retornar
@app.get("/api/cars/{id}")
def car_by_id(id: int) -> dict:
  result = [car for car in db if car.id==id]
  if result:
    return result[0]
  else:
    raise HTTPException(status_code=404, detail=f"No car with id {id} in the db")


@app.post("/api/cars")
def add_car(car: CarInput) -> CarOutput:
  new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, 
                      transmission=car.transmission, id=len(db)+1)
  db.append(new_car)
  save_db(db)
  return new_car








# permite correr el programa solo con el boton de play
if __name__ == "__main__":
  uvicorn.run("carsharing:app", reload=True)