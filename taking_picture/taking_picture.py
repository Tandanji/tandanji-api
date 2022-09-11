from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile
from pydantic import BaseModel
from model.detect import FoodModel

import string
import random
import os
import pandas as pd

router = APIRouter(prefix="/taking-pictures",tags=["pictures"],responses={404:{"description":"Not found"}})

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def render_takingPicturePage(request:Request):
  return templates.TemplateResponse("foodguide.html", {"request": request})

@router.post("/uploadfile")
async def create_upload_file(file: UploadFile, request:Request):
  folder_location = os.path.join(f"upload",id_generator())
  os.mkdir(folder_location)
  file_location = os.path.join(folder_location,file.filename)
  with open(file_location, "wb+") as file_object:
    file_object.write(file.file.read())
  strFoods=await activeModel(folder_location)
  food,cal=getFoodsByCSV(strFoods)
  '''url = f'{request.client.host}/?{params}'
  response = RedirectResponse(url=url)'''
  return {"predict": str(food)+" "+str(cal)}

def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

async def activeModel(folder_location):
    model=FoodModel(folder_location)
    return await model.detect()

def getFoodsByCSV(strFoods):
  foodlist=strFoods.split()
  dataFrame=pd.read_csv("model/caldata/caldata.csv")
  foodData=[]
  calData=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for index in foodlist:
    data=list(dataFrame[dataFrame["food"]==index].iloc[0])
    foodData.append(data[0])
    calData=[x+y for x,y in zip(calData, data[1:])]
  return [foodData,calData]


#음 식 명,중량(g),에너지(kcal),탄수화물(g),당류(g),지방(g),단백질(g),칼슘(mg),인(mg),나트륨(mg),칼륨(mg),마그네슘(mg),철(mg),아연(mg),콜레스테롤(mg),트랜스지방(g)
