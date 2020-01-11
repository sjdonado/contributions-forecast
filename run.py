import os
from app import app

if __name__ == "__main__":
  app.run(host = os.environ['HOSTNAME'], port = os.environ['PORT'], debug = True)