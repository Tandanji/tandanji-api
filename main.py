
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import taking_picture.taking_picture as taking_picture
import analysis.controller.analysis_controller as analysis_controller

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(taking_picture.router)
app.include_router(analysis_controller.router)

@app.get("/")
async def render_indexPage(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})