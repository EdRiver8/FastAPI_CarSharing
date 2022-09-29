import json
from pydantic import BaseModel

class Car(BaseModel):
  id: int
  size: str
  fuel: str
  doors: int
  transmission: str
  
  
def load_db() -> list[Car]:
  """Load a list of Car Objects from a JSON file"""
  with open("cars.json") as f:
    # haga esto 'Car.parse...' para cada 'obj' en el archivo 'f' transformado a json...
    return [Car.parse_obj(obj) for obj in json.load(f)]