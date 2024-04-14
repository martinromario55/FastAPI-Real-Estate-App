import sqlalchemy as sql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True, index=True)
    email = sql.Column(sql.String(255), unique=True,index=True)
    password = sql.Column(sql.String, nullable=False)
    is_active = sql.Column(sql.Boolean, default=True)
    is_verified = sql.Column(sql.Boolean, default=False)
    date_joined = sql.Column(sql.TIMESTAMP(timezone=True), server_default=text('now()'))
    
    
class UserOneTimePassword(Base):
    __tablename__ = "user_otp"
    
    
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True, index=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"), nullable=False)
    code = sql.Column(sql.String(6), nullable=False, unique=True)
    is_valid=sql.Column(sql.Boolean, default=True)