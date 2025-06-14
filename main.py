from flask import Flask
from config.settings import db, DATABASE_URL
from app.routes import inventory_bp

def create_app():
    app = Flask(__name__, template_folder="app/templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # for further tailoring, i should add alembic to modify existing tables changed columns and whatnot.
    with app.app_context():
        db.create_all()


    # here i can still add other blueprints for routes of the application
    app.register_blueprint(inventory_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)