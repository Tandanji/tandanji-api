from firebase.authentication import Authentication


class AuthenticationService:
  async def getAccountInfoAfterSignIn(self,email,password):
    return Authentication().signIn(email,password)

  async def getAccountInfoAfterSingUp(self,email,password):
    return Authentication().signUp(email,password)
