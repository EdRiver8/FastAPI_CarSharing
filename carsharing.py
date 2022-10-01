import uvicorn

from sqlmodel import create_engine, SQLModel, Session, select

from fastapi import FastAPI, HTTPException, Depends

import db_array
from schemas import Car, CarInput, CarOutput, TripInput, TripOutput, Trip,load_db, save_db

app = FastAPI(title="Car Sharing") # app = Rest service

# db_array = db_array.db
# db = load_db()

engine = create_engine(
  "sqlite:///carsharing.db", # string de coneccion
  connect_args={"check_same_thread": False}, # Needed for SQLite
  echo=True # Log generated SQL y los muestra por consola
)

# inicia antes de cualquier request del cliente
@app.on_event("startup")
def on_startup():
  SQLModel.metadata.create_all(engine) # cheque si la db existe, sino la crea

# sirve como inyeccion de dependencias
def get_session():
  with Session(engine) as session:
    yield session # funcion generadora, da proteccion de rollback en caso que algo salga mal


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
  
# usando sqlite
@app.get("/api/cars")
def get_cars(size: str|None = None, doors: int|None = None,
             session: Session = Depends(get_session)) -> list: # tipo de retorno es una lista
  query = select(Car) # una query que selecciona datos de un objeto Car
  if size:
    query = query.where(Car.size == size)
  if doors:
    query = query.where(Car.doors == doors)
  return session.exec(query).all()


#al especificar el tipo de dato con 'type hints' python nos ayuda para saber que se debe enviar o retornar
@app.get("/api/cars/{id}", response_model=Car)
def car_by_id(id: int,
             session: Session = Depends(get_session)) -> Car:
  car = session.get(Car, id)
  if car:
    return car
  else:
    raise HTTPException(status_code=404, detail=f"No car with id {id} in the db")


# funciona con db en json file
# @app.post("/api/cars", response_model=CarOutput)
# def add_car(car: CarInput) -> CarOutput:
#   new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, 
#                       transmission=car.transmission, id=len(db)+1)
#   db.append(new_car)
#   save_db(db)
#   return new_car

# funciona con sqlite
@app.post("/api/cars", response_model=Car)
def add_car(car_input: CarInput,
             session: Session = Depends(get_session)) -> Car:
  # trasaccion con la db, o todo esta bueno y se guarda o algo falla y no se guarda en la db
  new_car = Car.from_orm(car_input) # permite trabajara correctamente con relaciones entre objetos
  session.add(new_car)
  session.commit()
  session.refresh(new_car) # en esta parte se crea el id cuando se salva en la db
  return new_car
  

@app.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int,
             session: Session = Depends(get_session)) -> None:
  car = session.get(Car, id)
  if car:
    session.delete()
    session.commit()
  else:
    raise HTTPException(status_code=404, detail=f"No car with id = {id}")
  

@app.put("/api/cars/{id}", response_model=Car)
def change_car(id: int, new_data: CarInput,
             session: Session = Depends(get_session)) -> Car:
  car = session.get(Car, id)
  if car:
    car.fuel = new_data.fuel
    car.transmission = new_data.transmission
    car.size = new_data.size
    car.doors = new_data.doors
    session.commit()
    return car
  else:
    raise HTTPException(status_code=404, detail=f"No car with id = {id}")


@app.post("/api/cars/{car_id}/trips", response_model=Trip)
def add_trip(car_id: int, trip_input: TripInput,
             session: Session = Depends(get_session)) -> Trip:
  car = session.get(Car, car_id)
  if car:
    new_trip = Trip.from_orm(trip_input, update={'car_id': car_id})
    car.trips.append(new_trip)
    session.commit()
    session.refresh(new_trip)
    return new_trip
  else:
    raise HTTPException(status_code=404, detail=f"No car with id = {id}")





# permite correr el programa solo con el boton de play
if __name__ == "__main__":
  uvicorn.run("carsharing:app", reload=True)