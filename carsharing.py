from datetime import datetime

import uvicorn

from fastapi import FastAPI

import db_array

db = db_array.db

app = FastAPI() # app = Rest service

# @app.get("/api/cars")
# def get_cars():
#   return db;

# buscando por el size del car y cantidad de puertas
@app.get("/api/cars")
def get_cars(size: str|None = None, doors: int|None = None) -> list: # tipo de retorno es una lista
  result = db
  if size:
    result = [car for car in result if car['size'] == size];
  if doors:
    result = [car for car in result if car['doors'] >= doors]
  else: 
    return result

@app.get("/api/cars/{id}")
def car_by_id(id: int):
  result = [car for car in db if car['id']==id]
  return result[0]








if __name__ == "__main__":
  uvicorn.run("carsharing:app", reload=True)