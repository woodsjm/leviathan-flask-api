from flask import Flask, g


DEBUG = True
PORT = 8000

app = Flask(__name__, static_url_path="", static_folder="static")

@app.route('/')
def index():
    return 'SERVER IS WORKING'

if __name__ == '__main__':
  # models.initialize()
  app.run(debug=DEBUG, port=PORT, host='0.0.0.0')
