from fastapi import FastAPI

import authentication.controller.authentication_controller as authentication_controller

app = FastAPI()

app.include_router(authentication_controller.router)