import logging
from config import Config
from flask import Flask
from flask_session import Session

global logger

sess = Session()
logger = logging.getLogger(__name__)

if Config.FLASK_ENV == 'development':
  logging.basicConfig(filename='info.log',level=logging.INFO)

def create_app():
  """Construct the core application."""
  app = Flask(__name__, instance_relative_config=False)

  # Application Configuration
  app.config.from_object(Config)

  # Initialize Plugins
  sess.init_app(app)

  with app.app_context():
    # Import parts of our application
    from . import oauth
    from . import routes
    app.register_blueprint(routes.main_bp)
    app.register_blueprint(oauth.oauth_bp)

    return app