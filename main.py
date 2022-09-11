
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import taking_picture.controller.taking_picture_controller as taking_picture_controller
import analysis.controller.analysis_controller as analysis_controller

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(taking_picture_controller.router)
app.include_router(analysis_controller.router)

@app.get("/")
async def render_indexPage(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})