# Authentication Steps
Esses passos descrevem como o usuario irá logar na aplicação

- The endpoint /auth will receive a 'username,' which is the email, and a 'password.' Then, if the user has the field is_verified == True:
  - If true, it will return an access_token and a refresh_token.
  - If false, it will return an object with error == True and details describing the user's state (not registered or email not verified).

