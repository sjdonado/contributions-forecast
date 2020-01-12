from flask import Flask
from flask_session import Session

sess = Session()

def create_app():
  """Construct the core application."""
  app = Flask(__name__, instance_relative_config=False)

  # Application Configuration
  app.config.from_object('config.Config')

  # Initialize Plugins
  sess.init_app(app)

  with app.app_context():
    # Import parts of our application
    from . import oauth
    from . import routes
    app.register_blueprint(routes.main_bp)
    app.register_blueprint(oauth.oauth_bp)

    return app