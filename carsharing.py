from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcom():
  return {'Mesagge':"Welcome to the Car Sharing service!"}