## Google mail service
Sending an email with google smtp requires an gmail account and an app password for that account. You can create an app password, following three simple steps:

01. Go to the two step verification option in your [Google Account page](myaccount.google.com/signinoptions/two-step-verification)
02. Select **App Passwords** in the end of the page
03. Create an app password
04. Create a .mail.env file with MAIL_USERNAME, MAIL_PASSWORD and MAIL_FROM variables

MAIL_USERNAME refers to the email address of the sender.<br>
MAIL_PASSWORD refers to the app password of the sender.<br>
MAIL_FROM refers to the email of the sender that is going to appear in the email the recipient is going to receive.<br>
NAME refers to the name of the sender.

