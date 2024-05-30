import os

from flask import Flask 

from .extensions import db
from .app import main

def create_app():
    app = Flask(__name__)

    #app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://sms_messages_user:leMmtPVKr4TFxdudP6hYBPWPSnKRtr7Q@dpg-ck624kgs0i2c73chms00-a.oregon-postgres.render.com/sms_messages'
    # postgres://prettyprinted_render_example_user:11vq6k72GmFJazhVpz3pFUko50djVZT1@dpg-ceukdhmn6mpglqdb4avg-a.oregon-postgres.render.com/prettyprinted_render_example

    #db.init_app(app)

    app.register_blueprint(main)

    return app
