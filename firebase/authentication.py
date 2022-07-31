from firebase_admin import auth

class Authentication:
  def signIn(self,email,password):
    return auth.sign_in_with_email_and_password(email,password)

  def signUp():
    user = auth.create_user(
    email='user@example.com',
    email_verified=False,
    phone_number='+15555550100',
    password='secretPassword',
    display_name='John Doe',
    disabled=False)
    print('Sucessfully created new user: {0}'.format(user.uid))
