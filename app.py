from flask import Flask, g, request, jsonify, session
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user
from playhouse.shortcuts import model_to_dict
from flask_cors import CORS

import logging

import os

import models


DEBUG = True
PORT = 8000


login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return None

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = 'RLAKJDRANDOM STRING'
login_manager.init_app(app)


CORS(app, origins=['http://localhost:3000', "https://leviathan-wakes-react.herokuapp.com"], supports_credentials=True)


logging.getLogger('flask_cors').level = logging.DEBUG

###########
# Routes #
###########

@app.route('/login', methods=["POST"])
def login():
    payload = request.get_json()

    try:
        user = models.User.get(models.User.email== payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})


@app.route('/logout', methods=["GET"])
def logout():
  print(session)
  session.pop('email', None)
  return jsonify(data={}, status={"code": 200, "message": "User successfully logged out"}) 


@app.route('/register', methods=["POST"])
def register():
  payload = request.get_json()
  print("PAYLOAD: ", payload)

  try:
    models.User.get(models.User.email == payload.get('email'))
    return jsonify(data={}, status={"code": 401, "message": "A user with that name exists"})

  except models.DoesNotExist:
    payload['password'] = generate_password_hash(payload['password']).decode('utf8')
    user = models.User.create(**payload)
    login_user(user)
    user_dict = model_to_dict(user)
    del user_dict['password']
    return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

##################################
# Connection and Initialization #
##################################

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    # header = response.headers
    # header['Access-Control-Allow-Origin'] = '*'
    """Close the database connection after each request."""
    print("Here's the response from the server!!: ", response)
    g.db = models.DATABASE
    g.db.close()
    return response

@app.route('/')
def index():
    return 'SERVER IS WORKING'

if 'ON_HEROKU' in os.environ:
  print('hitting')
  models.initialize()

if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT, host='0.0.0.0')
