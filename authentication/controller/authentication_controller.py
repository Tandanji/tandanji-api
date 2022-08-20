from fastapi import APIRouter
from pydantic import BaseModel
from ..service.authentication_service import AuthenticationService

router = APIRouter(prefix="/auth",tags=["auth"],responses={404:{"description":"Not found"}})

class SignData(BaseModel):
  email:str
  password:str

@router.get("/id/{id}/pwd/{pwd}")
async def signIn(email:str,password:str):
  return AuthenticationService().getAccountInfoAfterSignIn(email,password)

@router.post("/")
async def signUp(signData:SignData):
  return AuthenticationService().getAccountInfoAfterSingUp(signData.email,signData.password)