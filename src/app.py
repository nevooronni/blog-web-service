from flask import Flask

from .config import app_config
from .models import db, bcrypt

#import user_api blueprint
from .views.UserView import user_api as user_blueprint

def create_app(env_name):
  """
    create app
  """

  #app initialization
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  #wrap db and bcypt with app and initialize them
  bcrypt.init_app(app)
  db.init_app(app)

  #register user_lueprint
  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')

  @app.route('/', methods=['GET'])
  def index():
    """
      example endpoint
    """
    return 'congradulations! Your first endpoint is working'

  return app
