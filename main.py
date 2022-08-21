
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import authentication.controller.authentication_controller as authentication_controller

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(authentication_controller.router)
@app.get("/")
async def render_indexPage(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})


