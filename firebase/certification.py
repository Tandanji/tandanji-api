import os
import firebase_admin
from firebase_admin import credentials

class Certification:
  def __init__(self) -> None:
    rootPath=os.path.dirname(os.path.abspath(__file__))
    keyPath=os.path.join(rootPath,'tandanji-firebase-adminsdk-mdoh5-4397eb439b.json')
    cred=credentials.Certificate(keyPath)
    firebase_admin.initialize_app(cred)
