
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import authentication.controller.authentication_controller as authentication_controller
import taking_pictures.controller.taking_pictures_controller as taking_pictures_controller
import food_listing.controller.food_listing_controller as food_listing_controller
import analysis.controller.analysis_controller as analysis_controller

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(authentication_controller.router)
app.include_router(taking_pictures_controller.router)
app.include_router(food_listing_controller.router)
app.include_router(analysis_controller.router)

@app.get("/")
async def render_indexPage(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})