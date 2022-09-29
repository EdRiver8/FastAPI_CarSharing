from datetime import datetime

from fastapi import FastAPI

import db_array

app = FastAPI() # app = Rest service

@app.get("/")
def welcom(name):
  return {'Mesagge': f"Welcome {name} to the Car Sharing service!"}

@app.get("/date")
def welcom():
  return {'date': datetime.now()}

