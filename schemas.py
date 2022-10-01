# python -m pip install sqlmodel

# import json
# from pydantic import BaseModel # se reemplaza x SQLmodel que hereda de pydantic
from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])


class TripInput(SQLModel):
  start: int
  end: int
  description: str
  
  
class TripOutput(TripInput):
  id: int


class Trip(TripInput, table=True):
  id: int | None = Field(default=None, primary_key=True)
  # no es optional '|None' xq para q hayan viajes, debe existir 1 carro que los realice
  car_id: int = Field(foreign_key="car.id")# id del carro que le pertene este 'Trip'
  # 'Car' es un string, porque la clase 'Car' esta debajo de 'Trip' en este archivo,
  #  lo que hace que cuando python lea el codido la clase 'Car' no existe aun,
  # asi que no podemos usar una variable, por ello se usa un string y luego cuando
  # la clase exista sera usada como el type hint
  # back_populates, significa que la misma relacion existe en la clase 'Car',
  # con un atributo llamado 'trips'
  car: "Car" = Relationship(back_populates="trips") 


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
    
# Hereda de CarInput pero le agrega el id y es muy similar a 'Car', solo que 
# CarInput es un Schema que determina que se datos se enviaran por internet
class CarOutput(CarInput):
  id: int
  trips: list[TripOutput] = []

# con table=true, se vuelve un modelo de datos que se envia a la db
class Car(CarInput, table=True):
  # solo cuando se salve el car en la db se crea el id
  id: int | None =  Field(primary_key=True, default=None)
  trips: list[Trip] = Relationship(back_populates="car") # muchos viajes a un carro
  
  
class User(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
  password_hash: str = ""  # python -m pip install "passlib[bcrypt]"
  
  def set_password(self, password):
    """Setting the passwords actually sets password_hash."""
    self.password_hash = pwd_context.hash(password)

  def verify_password(self, password):
    """Verify given password by hashing and comparing to password_hash."""
    return pwd_context.verify(password, self.password_hash)
  
  
class UserOutput(SQLModel):
  id: int
  username: str

  
# def load_db() -> list[CarOutput]:
#   """Load a list of CarInput Objects from a JSON file"""
#   with open("cars.json") as f:
#     # haga esto 'Car.parse...' para cada 'obj' en el archivo 'f' transformado a json...
#     return [CarOutput.parse_obj(obj) for obj in json.load(f)]
  
# def save_db(cars: list[CarInput]):
#   with open("cars.json", 'w') as f:
#     #cada carro de la lista cars, lo convierte en un dict con espaciado 4
#     json.dump([car.dict() for car in cars], f, indent=4)