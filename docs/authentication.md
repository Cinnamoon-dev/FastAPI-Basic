# Authentication Steps
Esses passos descrevem como o usuario irá logar na aplicação

- It will provide a 'username,' which is the email, and a 'password.' After selection, if the user has the field is_verified == True:

  - If true, they will receive an access_token and a refresh_token.
  - If false, they will receive an object with error == True and details describing the user's state (not registered or email not selected).

