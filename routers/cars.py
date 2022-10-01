from sqlmodel import Session, select

from fastapi import HTTPException, Depends, APIRouter

from db import get_session
from schemas import Car, CarInput, CarOutput, TripInput, Trip

router = APIRouter(prefix="/api/cars") # evitar circular importacion generado por 'app'

# usando sqlite
@router.get("/")
def get_cars(size: str|None = None, doors: int|None = None,
             session: Session = Depends(get_session)) -> list: # tipo de retorno es una lista
  query = select(Car) # una query que selecciona datos de un objeto Car
  if size:
    query = query.where(Car.size == size)
  if doors:
    query = query.where(Car.doors == doors)
  return session.exec(query).all()


#al especificar el tipo de dato con 'type hints' python nos ayuda para saber que se debe enviar o retornar
@router.get("/{id}", response_model=CarOutput)
def car_by_id(id: int,
             session: Session = Depends(get_session)) -> Car:
  car = session.get(Car, id)
  if car:
    return car
  else:
    raise HTTPException(status_code=404, detail=f"No car with id {id} in the db")

# funciona con sqlite
@router.post("/", response_model=Car)
def add_car(car_input: CarInput,
             session: Session = Depends(get_session)) -> Car:
  # trasaccion con la db, o todo esta bueno y se guarda o algo falla y no se guarda en la db
  new_car = Car.from_orm(car_input) # permite trabajara correctamente con relaciones entre objetos
  session.add(new_car)
  session.commit()
  session.refresh(new_car) # en esta parte se crea el id cuando se salva en la db
  return new_car
  

@router.delete("/{id}", status_code=204)
def remove_car(id: int,
             session: Session = Depends(get_session)) -> None:
  car = session.get(Car, id)
  if car:
    session.delete()
    session.commit()
  else:
    raise HTTPException(status_code=404, detail=f"No car with id = {id}")
  

@router.put("/{id}", response_model=Car)
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
  
  
class BadTripException(Exception):
    pass


@router.post("/{car_id}/trips", response_model=Trip)
def add_trip(car_id: int, trip_input: TripInput,
             session: Session = Depends(get_session)) -> Trip:
    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.from_orm(trip_input, update={'car_id': car_id})
        if new_trip.end < new_trip.start:
            raise BadTripException("Trip end before start")
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")
  
  
  
# funciona con db en json file
# @router.post("/api/cars", response_model=CarOutput)
# def add_car(car: CarInput) -> CarOutput:
#   new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, 
#                       transmission=car.transmission, id=len(db)+1)
#   db.append(new_car)
#   save_db(db)
#   return new_car