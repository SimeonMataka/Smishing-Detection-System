from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
#from .app import main

db = create_engine('postgresql://sms_messages_user:leMmtPVKr4TFxdudP6hYBPWPSnKRtr7Q@dpg-ck624kgs0i2c73chms00-a/sms_messages')
Session = sessionmaker(bind=db)

#db_session = scoped_session(Session)
