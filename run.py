from app import app
from config import Config

if __name__ == "__main__":
  app.run(host = Config.HOSTNAME, port = Config.PORT, debug = Config.DEBUG)