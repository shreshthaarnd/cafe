# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACf3a2e9573dd9b2e6a490307861cf0bb3'
auth_token = '2ca15d26918becf33890f05b75de7ba3'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+12056795952',
                              body='Testing from python',
                              to='+919014994442'
                          )

print(message.sid)