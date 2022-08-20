from firebase.authentication import Authentication

class AuthenticationService:
  async def getAccountInfoAfterSignIn(email,password):
    return Authentication().signIn(email,password)

  async def getAccountInfoAfterSingUp(email,password):
    return Authentication().signUp(email,password)