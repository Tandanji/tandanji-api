from authentication.service.authentication_service import AuthenticationService
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

router = APIRouter(prefix="/auth",tags=["auth"],responses={404:{"description":"Not found"}})

templates = Jinja2Templates(directory="templates")

class SignData(BaseModel):
  email:str
  password:str

@router.get("/", response_class=HTMLResponse)
def render_loginPage(request:Request):
  return templates.TemplateResponse("login.html", {"request": request})

@router.get("/id/{id}/pwd/{pwd}")
async def signIn(email:str,password:str):
  return AuthenticationService().getAccountInfoAfterSignIn(email,password)

@router.post("/")
async def signUp(signData:SignData):
  return AuthenticationService().getAccountInfoAfterSingUp(signData.email,signData.password)
