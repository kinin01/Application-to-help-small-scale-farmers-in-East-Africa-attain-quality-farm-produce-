from twilio.rest import Client

account_sid ='AC05b129e0da13e7b1ec1b955fccbf527a'
auth_token ='4fc821e8c089c82df7a8bd8ff4d80ac7'

twilio_number='+17817982730'
my_phone_number =''


client = Client(account_sid, auth_token)

def send_message(message,phone_number):
    message = client.messages.create(
        from_=twilio_number,
        body= message,
        to= phone_number,
    )
    return message
