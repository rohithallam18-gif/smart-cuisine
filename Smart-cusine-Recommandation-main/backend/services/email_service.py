import random
from flask_mail import Message
from extensions import mail

def send_email_otp(receiver_email, otp):
    try:
        msg = Message(
            subject="Smart Cuisine OTP Verification",
            recipients=[receiver_email],
            body=f"Your verification code is: {otp}\n\nThis code will expire in 2 minutes."
        )
        mail.send(msg)
        return True
    except Exception as e:
        print("EMAIL ERROR:", e)
        return False

def generate_otp():
    return str(random.randint(100000, 999999))
