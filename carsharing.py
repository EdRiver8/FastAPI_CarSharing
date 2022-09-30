import uvicorn

from fastapi import FastAPI, HTTPException

import db_array
from schemas import CarInput, CarOutput, TripInput, TripOutput, load_db, save_db

db_array = db_array.db
db = load_db()

app = FastAPI(title="Car Sharing") # app = Rest service

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


@app.post("/api/cars", response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
  new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, 
                      transmission=car.transmission, id=len(db)+1)
  db.append(new_car)
  save_db(db)
  return new_car

@app.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int) -> None:
  matches = [car for car in db if car.id == id]
  if matches:
    car = matches[0];
    db.remove(car);
    save_db(db)
  else:
    raise HTTPException(status_code=404, detail=f"No car with id = {id}")
  

@app.put("/api/cars/{id}")
def change_car(id: int, new_data: CarInput) -> CarOutput:
  matches = [car for car in db if car.id == id]
  if matches:
    car = matches[0]
    car.fuel = new_data.fuel
    car.transmission = new_data.transmission
    car.size = new_data.size
    car.doors = new_data.doors
    save_db(db)
    return car
  else:
    raise HTTPException(status_code=404, detail=f"No car with id = {id}")


@app.post("/api/cars/{car_id}/trips", response_model=TripOutput)
def add_trip(car_id: int, trip: TripInput) -> TripOutput:
  matches = [car for car in db if car.id == id]
  if matches:
    car = matches[0]
    new_trip = TripOutput(id=len(car.trips)+1, start=trip.start, 
                          end=trip.end, description=trip.description)
    car.trips.append(new_trip)
    save_db(db)
    return new_trip
  else:
    raise HTTPException(status_code=404, detail=f"No car with id = {id}")







# permite correr el programa solo con el boton de play
if __name__ == "__main__":
  uvicorn.run("carsharing:app", reload=True)