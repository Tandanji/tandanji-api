from typing import Union

from fastapi import FastAPI

from firebase.repository import Repository
from firebase.certification import Certification
from firebase.authentication import Authentication

app = FastAPI()
Certification()


@app.get("/")
def read_root():
  repo=Repository()
  auth=Authentication()
  print(auth.signIn("asdf","qwer"))
  repo.setData()
  return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id1": item_id, "q": q}