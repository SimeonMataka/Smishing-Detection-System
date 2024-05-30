from .extensions import db 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class SMSMessage(Base):
    __tablename__ = 'sms_message'
    
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    result = Column(String(20))
