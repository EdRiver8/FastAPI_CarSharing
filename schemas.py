# python -m pip install sqlmodel

import json
# from pydantic import BaseModel # se reemplaza x SQLmodel que hereda de pydantic
from sqlmodel import SQLModel, Field

class CarInput(SQLModel):
  size: str
  fuel: str | None = "electric"
  doors: int
  transmission: str | None = "auto"
  
  class Config:
    schema_extra = {
      "example": {
        "size" : "m",
        "doors" : 5,
        "transmission" : "manual",
        "fuel" : "gasoline",
      }
    }

# con table=true, se vuelve un modelo de datos que se envia a la db
class Car(CarInput, table=True):
  # solo cuando se salve el car en la db se crea el id
  id: int | None =  Field(primary_key=True, default=None)
  
  

class TripInput(SQLModel):
  start: int
  end: int
  description: str
  
  
class TripOutput(TripInput):
  id: int
  
# Hereda de CarInput pero le agrega el id y es muy similar a 'Car', solo que 
# CarInput es un Schema que determina que se datos se enviaran por internet
class CarOutput(CarInput):
  id: int
  trips: list[TripOutput] = []
  
  
def load_db() -> list[CarOutput]:
  """Load a list of CarInput Objects from a JSON file"""
  with open("cars.json") as f:
    # haga esto 'Car.parse...' para cada 'obj' en el archivo 'f' transformado a json...
    return [CarOutput.parse_obj(obj) for obj in json.load(f)]
  
def save_db(cars: list[CarInput]):
  with open("cars.json", 'w') as f:
    #cada carro de la lista cars, lo convierte en un dict con espaciado 4
    json.dump([car.dict() for car in cars], f, indent=4)