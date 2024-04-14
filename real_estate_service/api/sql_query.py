from sqlalchemy.orm import Session
from . import models, schema


# Check if user exists
async def check_user_exists(db: Session, email: str,):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user


# Create user
def insert_user(db: Session, user: schema.UserCreate):
    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Create OTP
def create_otp_for_user(db: Session, otp: schema.OTPData):
    new_otp = models.UserOneTimePassword(user_id=otp.user_id, code=otp.code)
    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)
    return new_otp