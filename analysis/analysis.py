from typing import Union
from fastapi import APIRouter, Request, Cookie
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json

router = APIRouter(prefix="/analysis",tags=["auth"],responses={404:{"description":"Not found"}})

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def render_loginPage(request:Request,nutrient: Union[str, None] = Cookie(default=None)):
  if(nutrient==None):
    return RedirectResponse("/taking-pictures",status_code=200)
  jsonNutrient=eval(nutrient)
  return templates.TemplateResponse("analysis.html", {"request": request,"percent":jsonNutrient["percent"],"value":jsonNutrient["value"]})