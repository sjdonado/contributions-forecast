from flask import Flask
from flask_session import Session
from config import Config

sess = Session()

app = Flask(__name__, instance_relative_config=False)
app.config.from_object(Config)
sess.init_app(app)

from . import views
from . import api