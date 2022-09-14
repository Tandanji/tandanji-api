from calendar import c
from urllib import response
from fastapi import APIRouter, Request, Response ,Form, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile
from pydantic import BaseModel
from model.detect import FoodModel
import numpy as np
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
async def create_upload_file(file: UploadFile=File(...), gender:str=Form(...),age:int=Form(...)):
  folder_location = os.path.join(f"upload",id_generator())
  os.mkdir(folder_location)
  file_location = os.path.join(folder_location,file.filename)
  with open(file_location, "wb+") as file_object:
    file_object.write(file.file.read())
  strFoods=await activeModel(folder_location)
  food,cal=getFoodsByCSV(strFoods)
  recommendNutrient=getNutrientByCSV(gender,age)
  currentPercent=calcPercent(recommendNutrient,cal)

  headers = {"percent": "/".join(map(str,currentPercent)),"value":"/".join(map(str,cal)) }
  response = RedirectResponse('/analysis', status_code=303)
  response.set_cookie(key="nutrient", value=headers)
  return response

def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

async def activeModel(folder_location):
    model=FoodModel(folder_location)
    return await model.detect()

def getFoodsByCSV(strFoods):
  foodlist=strFoods.split()
  dataFrame=pd.read_csv("model/caldata/caldata.csv")
  foodData=[]
  calData=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for index in foodlist:
    data=list(dataFrame[dataFrame["food"]==index].iloc[0])
    foodData.append(data[0])
    calData=[round(x+y,0) for x,y in zip(calData, data[2:])]
  return [foodData,calData]

def getNutrientForGender(gender):
  filePath="model/nutrient-data/man_nutrient.csv"
  if(gender=="male"):
    filePath="model/nutrient-data/woman_nutrient.csv"
  return filePath

def getNutrientByCSV(gender,age):
  filePath=getNutrientForGender(gender)
  nutrientData=pd.read_csv(filePath)
  nutrientList=list(nutrientData[(nutrientData["start"] < age) & (age <= nutrientData["end"])].iloc[0])
  return nutrientList[2:]

def calcPercent(recommendNutrientList, currentNutrientList):
  data=[round((current/recommend)*100,0) for recommend,current in zip(recommendNutrientList, currentNutrientList)]
  return np.nan_to_num(data,copy=True,posinf=0)

  

  



#음 식 명,중량(g),에너지(kcal),탄수화물(g),당류(g),지방(g),단백질(g),칼슘(mg),인(mg),나트륨(mg),칼륨(mg),마그네슘(mg),철(mg),아연(mg),콜레스테롤(mg),트랜스지방(g)
