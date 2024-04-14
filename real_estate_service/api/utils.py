from passlib.context import CryptContext
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from typing import List

import pyotp

from .config import get_settings

settings = get_settings()


conf = ConnectionConfig(
    MAIL_USERNAME =f"{settings.mail_username}",
    MAIL_PASSWORD = f"{settings.mail_password}",
    MAIL_FROM = f"{settings.mail_from}",
    MAIL_PORT = 456,
    MAIL_SERVER = f"{settings.mail_server}",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

pwd_context = CryptContext(schemes=['bcrypt'])

# Email confirmation
def send_email(background_task: BackgroundTasks, subject:str, recipient: List, message: str):
    message = MessageSchema(
        subject=subject,
        body=message,
        recipients=recipient,
        subtype='html'
    )
    fm = FastMail(conf)
    background_task.add_task(fm.send_message, message)


# Hash Password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Generate OTP
secret = pyotp.random_base32()
time_otp = pyotp.TOTP(secret, interval=180) # Three minute interval (180 seconds)

def generate_otp():
    return time_otp.now()

# Verify OTP
def verify_otp(code):
    return time_otp.verify(code)