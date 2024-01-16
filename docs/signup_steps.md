## Signup Steps
The signup process is composed by two steps in the client side:

- Create account putting their data in the api
- Clicking a link in their email 

In the server side, the process is composed by more steps:

- Creating a row in the users table
- The user created has a field `isVerified = False`
- Generating a link with a token that will be sent to the user's email to call the `verify_email` endpoint
- Send the email to the user's email address using FastAPI SMTP
- Serialize the token and set `isVerified = True`