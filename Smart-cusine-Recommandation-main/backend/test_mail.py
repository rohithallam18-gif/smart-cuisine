import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

username = os.environ.get('MAIL_USERNAME')
password = os.environ.get('MAIL_PASSWORD')

print(f"Testing SMTP login for: {username}")
print(f"Password length: {len(password) if password else 0}")

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    print("Login successful!")
    
    msg = MIMEText("Test email from Smart Food.")
    msg['Subject'] = "Test OTP"
    msg['From'] = username
    msg['To'] = username
    
    server.send_message(msg)
    print("Test email sent!")
    server.quit()
except Exception as e:
    print(f"Failed: {e}")
