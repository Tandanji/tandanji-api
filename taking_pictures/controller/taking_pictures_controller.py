from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

router = APIRouter(prefix="/taking-pictures",tags=["pictures"],responses={404:{"description":"Not found"}})

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def render_takingPicturePage(request:Request):
  return templates.TemplateResponse("foodguide.html", {"request": request})