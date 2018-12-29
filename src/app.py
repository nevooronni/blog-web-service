from flask import Flask

from .config import app_config

def create_app(env_name):
  """
    create app
  """

  #app initialization
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  @app.route('/', methods=['GET'])
  def index():
    """
      example endpoint
    """
    return 'congradulations! Your first endpoint is working'

  return app
