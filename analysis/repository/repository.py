import pyrebase
import json

class Repository:
  def __init__(self):
    with open('./firebase-info.json') as f:
      self.config = json.load(f)
      self.firebase = pyrebase.initialize_app(self.config)

  def getData(self):
    db=self.firebase.database()
    return db.child("users").get()

  def setData(self):
    db=self.firebase.database()
    data={
      "name":"jaejun",
      "desc":"helloworld",
      "age":123
    }
    return db.child("users").push(data)


#from firebase.repository import Repository