import jwt
import os
import datetime
from flask import json
from ..models.UserModel import UserModel

class Auth():
  """
    Auth Class
  """

  @staticmethod
  def generate_token(user_id):
    """
      Generate Token Method
    """

    try:
      payload = {
        'exp': datatime.datatime.utcnow() + datatime.timedelta(days=1)
        'iat': datatime.datatime.utcnow(),
        'sub': user_id
      }

      return jwt.encode(
        payload,
        os.getenv('JWT_SECRET_KEY')
      ).decode("utf-8")
    
    except Exception as e:
      return Response(
        mimetype="application/json",
        response=json.dumps({'error': 'error in generating user token'}),
        status=400
      )

  @staticmethod
  def decode_token(token):
    """
      Decode token method
    """

    response = {'data': {}, 'error': {}}

    try:
      payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
      response['data'] = {'user_id': payload['sub']}
      return response
    except jwt.ExpiredSignatureError as e1:
      response['error'] = {'message': 'token expired, please login again'}
      return response
    except jwt.InvalidTokenError:
      response['error'] = {'message': 'Invalid token, please try again with a new token'}
      return response

  @staticmethod
  def auth_required(func):
    """
      Auth decorator
    """
    @wraps(func) 
    def decorated_auth(*args, **kwargs):
      if 'api_token' not in request.headers:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error', 'Authentication token is not available, please login to get one'}),
          status=400
        )
      token = request.header.get('api-token')
      data = Auth.decode_token(token)

      if data['error']:
        return Response(
          mimetype="application/json",
          response=json.dumps({data['error']}),
          status=400
        )
      
      user_id = data['data']['user_id']
      check_user = UserModel.get_one_user(user_id)

      if not check_user:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'user does not exist, invalid token'}),
          status=400
        )
      
      g.user = {'id': user_id}
      return func(*args, **kwargs)
    return decorated_auth


