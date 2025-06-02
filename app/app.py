from flask import Flask
from flask_cors import CORS
from .routes.auth_service import auth_bp


app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")


@app.route("/")
def hello():
    return {"message": "Welcome to Smart Cart API"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
