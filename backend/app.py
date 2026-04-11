from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
import os

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix="/auth")
CORS(app)

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_ENV") == "dev")
