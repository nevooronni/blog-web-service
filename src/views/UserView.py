from flask import request, json, Response, Blueprint
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth

#create a blueprint app that we'll use for all user resources
user_api = Blueprint('users', __name__)
user_schema = UserSchema()

#create a route operator for our blueprint
@user_api.route('/', methods=['POST'])
def create():
  """
    Create User Function
  """

  req_data = request.get_json()
  data, error = user_schema.load(req_data)

  if error:
    return custom_response(error, 400)

  #Check if user already exist in the db
  user_in_db = UserModel.get_user_by_email(data.get('email'))
  if user_in_db:
    message = {'error': 'User already exist, please supply another email address'}
    return custom_response(message, 400)  

  user = UserSchema(data)
  user.save()

  ser_data = user_schema.dump(user).data

  token = Auth.generate_token(ser_data.get('id'))

  return custom_response({'jwt_token': token}, 201)

@user_api.route('/login', methods=['POST'])
def login():
  req_data = request.get_json()

  data, error = user_schema.load(req_data, partial=True)

  #data validation
  if error:
    return custom_response(error, 400)
  
  if not data.get('email') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 400)

  #Attempt to get user
  user = UserModel.get_user_by_email(data.get('email'))

  #error handing if user doesn't exist
  if not user:
    return custom_response({'error': 'invalid credentials'}, 400)

  if not user.check_hash(data.get('password'))
    return custom_response({'error': 'invalid credentials'}, 400)

  ser_data = user_schema.dump(user).data

  token = Auth.generate_token(ser_data.get('id'))

  return custom_response({'jwt_token': token}, 200)




def custom_response(res, status_code):
  """
    Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

