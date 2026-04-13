from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
import os
from dotenv import load_dotenv
from flask_migrate import Migrate

from models import db, User   # 👈 add this

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp, url_prefix="/auth")
CORS(app)

# quick DB test route
@app.route("/health/db")
def health_db():
    try:
        db.session.execute(db.text("SELECT 1"))
        return {"db": "connected"}
    except Exception as e:
        return {"db": "error", "details": str(e)}

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_ENV") == "dev")