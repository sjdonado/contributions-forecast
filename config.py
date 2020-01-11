from os import environ
import redis

class Config:
  # General Config
  SECRET_KEY = environ.get('SECRET_KEY')
  FLASK_ENV = environ.get('FLASK_ENV')
  DEBUG = FLASK_ENV == 'development'
  CLIENT_ID = environ.get('CLIENT_ID')
  CLIENT_SECRET = environ.get('CLIENT_SECRET')
  CALLBACK = environ.get('CALLBACK')

  # Flask-Session
  SESSION_TYPE = 'redis'
  SESSION_REDIS = redis.from_url(environ.get('REDIS'))