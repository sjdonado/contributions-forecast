from app import app
from config import Config

if __name__ == "__main__":
  if (Config.FLASK_ENV == 'production'):
    app.run()
  else:
    app.run(host = '0.0.0.0', debug = Config.DEBUG)