from fastapi import APIRouter, Request, Form, Depends, Cookie
from sqlmodel import Session
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import get_session
from routers.cars import get_cars

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, cars_cookie: str|None = Cookie(None)):
    print(cars_cookie)
    return templates.TemplateResponse("home.html",
                                      {"request": request})

# '*' convierte todo en keyword argumento, no importa que va antes o despues
@router.post("/search", response_class=HTMLResponse)
def search(*, size: str = Form(...), doors: int = Form(...),
           request: Request,
           session: Session = Depends(get_session)):
    cars = get_cars(size=size, doors=doors, session=session)
    return templates.TemplateResponse("search_results.html",
                                      {"request": request, "cars": cars})
  
  

  
  # return"""
  # <!DOCTYPE html>
  # <html lang="en">

  # <head>
  #   <meta charset="UTF-8">
  #   <meta http-equiv="X-UA-Compatible" content="IE=edge">
  #   <meta name="viewport" content="width=device-width, initial-scale=1.0">
  #   <title>Car Sharing</title>
  # </head>

  # <body>
  #   <h1>Welcome to the Car Sharing Services</h1>
  #   <p>Some Text!</p>

  # </body>

  # </html>
  # """
