from flask import Flask, g, request, jsonify
from flask_bcrypt import generate_password_hash
from flask_login import LoginManager, login_user
from playhouse.shortcuts import model_to_dict

import models


DEBUG = True
PORT = 8000

login_manager = LoginManager()
app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = 'RLAKJDRANDOM STRING'
login_manager.init_app(app)

###########
# Routes #
###########

@app.route('/register', methods=["POST"])
def register():

  payload = request.get_json()

  print(payload)
  # print(payload.get('email'))

  try:

    models.User.get(models.User.email == payload.get('email'))

    return jsonify(data={}, status={"code": 401, "message": "A user with that name exists"})

  except models.DoesNotExist:


    payload['password'] = generate_password_hash(payload['password']).decode('utf8')

    user = models.User.create(**payload)

    login_user(user)

    print("user")
    print(user)

    user_dict = model_to_dict(user)

    del user_dict['password']

    print("user_dict")
    print(user_dict)

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
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
    return 'SERVER IS WORKING'

if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT, host='0.0.0.0')
