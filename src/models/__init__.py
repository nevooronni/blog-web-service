from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

#initalize our db
db = SQLAlchemy()

#initialize Bcrypt
bcrypt = Bcrypt()