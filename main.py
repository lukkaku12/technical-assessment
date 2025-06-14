from flask import Flask
from config.settings import db, DATABASE_URL
from app.routes import inventory_bp

app = Flask(__name__, template_folder="app/templates")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(inventory_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)