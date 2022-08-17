from firebase_admin import auth

class Authentication:
  def signIn(self,email,password):
    return auth.sign_in_with_email_and_password(email,password)

  def signUp(self):
    user = auth.create_user(
    email='user123@example.com',
    password='secretPassword',
    display_name='John Doe',
    disabled=False)
    print('Sucessfully created new user: {0}'.format(user.uid))
