from flask import Flask # type: ignore

from main import main_bp
from user import user_bp
from admin import admin_bp

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = "gamegrid_secret"

app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
