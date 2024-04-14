from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks, Response
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schema, sql_query, utils, models

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["User Authentication"],
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user: schema.UserCreate, background_task: BackgroundTasks, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if email already exists
    result = await sql_query.check_user_exists(db, user.email)
    print(result)
    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.email} already exists",
        )
        
    # Hash password
    user.password = utils.hash_password(user.password)

    # Create user
    new_user = sql_query.insert_user(db, user)
    
    # Send email verification
    # otp
    otpcode = utils.generate_otp()
    otp_data = schema.OTPData
    otp_data.code = otpcode
    otp_data.user_id = new_user.id
    
    message="""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Email Verification</title>
        </head>
        <body>
            <div style="width: 100%; font-size: 16px; margin-top: 20px; text-align: center;">
                <h1>Email Verification</h1>
                <p>Please verify your email {0:}, with the otp code below</p><br>
                <span style="margin: 10px 6px; font-size: 16px; box-sizing: border-box; background: #f2f2f2;">{1:}</span>
                <p>Please note the otp code expires in 2 minutes after which it becomes invalid.</p>
            </div>
        </body>
    </html>
    """.format(user.email, otpcode)
    
    utils.send_email(background_task, subject="Verify your Email", recipient=[user.email], message=message)
    
    sql_query.create_otp_for_user(db, otp=otp_data)

    return {
        "message": "Account created successfully! Pleases verify your email with One Time Password sent to your email.",
    }
    
    
@router.post("/email-verification", status_code=status.HTTP_200_OK)
async def verify_email(otp: schema.OneTimePassword, response: Response, db: Session = Depends(get_db)):
    otp_user_qs = db.query(models.UserOneTimePassword).filter(models.UserOneTimePassword.code == otp.code)
    otp_user = otp_user_qs.first()
    
    isValid = utils.verify_otp(otp.code)
    # Check if OTP is valid and update user's feed
    if isValid and otp_user.is_valid:
        user_qs = db.query(models.User).filter(models.User.id == otp_user.user_id)
        user = user_qs.first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with id {otp_user.user_id} does not exist",
            )
            
        user_qs.update({"is_verified": True}, synchronize_session=False)
        otp_user_qs.update({"is_verified": False}, synchronize_session=False)
        
        db.commit()
        
        return {
            "status": "account verified successfully",
            "is_verified": user.is_verified
        }
        
    # If code is invalid
    else:
        otp_user_qs.update({"is_verified": False}, synchronize_session=False)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "message": "Invalid otp or otp has expired."
        }