from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/auth",tags=["auth"],responses={404:{"description":"Not found"}})

class SignUpData(BaseModel):
  email:str
  password:str
  nickname:str

@router.get("/")
async def signIn():
  return "";

@router.post("/")
async def signUp(userData:SignUpData):
  
  return "";