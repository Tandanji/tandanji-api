import json

import pyrebase


class Authentication:
  def __init__(self):
    with open('./firebase-info.json') as f:
      self.config = json.load(f)
      self.firebase = pyrebase.initialize_app(self.config)

  def signIn(self,email,password):
    signData=self.firebase.auth().sign_in_with_email_and_password(email,password)
    return self.firebase.auth().get_account_info(signData["idToken"])

  def signUp(self,email,password):
    signData=self.firebase.auth().create_user_with_email_and_password(email, password)
    return self.firebase.auth().get_account_info(signData["idToken"])



