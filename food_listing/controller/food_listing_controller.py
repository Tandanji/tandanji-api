from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

router = APIRouter(prefix="/food-listings",tags=["auth"],responses={404:{"description":"Not found"}})

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def render_loginPage(request:Request):
  return templates.TemplateResponse("foodlist.html", {"request": request})