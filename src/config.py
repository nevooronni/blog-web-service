import os

class Development(object):
  """
    Development environment configuration
  """
  DEBUG = True
  TESTING = False
  #do not want to expose the jwt_secret_key so secret variables need to be set in our system environment 
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class Production(object):
  """
    Production environment configurations
  """

  DEBUG = False
  TESTING = False
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
  JWT_SECRET_KEY = OS.getenv('JWT_SECRET_KEY')

app.config = {
  'development': Development,
  'production': Production
}