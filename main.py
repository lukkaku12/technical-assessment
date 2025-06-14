from flask import Flask
from app.routes import inventory_bp

app = Flask(__name__)
app.register_blueprint(inventory_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)