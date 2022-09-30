import json
from pydantic import BaseModel

class CarInput(BaseModel):
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

class TripInput(BaseModel):
  start: int
  end: int
  description: str
  
  
class TripOutput(TripInput):
  id: int
  
# Hereda de CarInput pero le agrega el id
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