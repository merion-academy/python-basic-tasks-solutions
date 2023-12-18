# Проект

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from core.auth import login_manager
from core.models import db
from views.auth import auth_app
from views.categories import categories_app
from views.movies import movies_app

app = Flask(__name__)
app.config.update(
    # python -c 'import secrets; print(secrets.token_hex())'
    SECRET_KEY="18e3f12a122aca34791cb76c8a544e840c7d1060f822a3b303a8d672e331765d",
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg://user:password@localhost:5432/cinema",
)
app.register_blueprint(auth_app)
app.register_blueprint(categories_app)
app.register_blueprint(movies_app)

csrf = CSRFProtect(app)
login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.get("/", endpoint="index")
def cinema_index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
