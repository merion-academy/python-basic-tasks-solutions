# Самостоятельная работа №7

from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from views.quotes import quotes_app

from models import db


app = Flask(__name__)
app.config.update(
    # python -c 'import secrets; print(secrets.token_hex())'
    SECRET_KEY="18e3f12a122aca34791cb76c8a544e840c7d1060f822a3b303a8d672e331765d",
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg://user:password@localhost:5432/quotes",
)
app.register_blueprint(quotes_app)


csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.get("/", endpoint="index")
def index():
    return redirect(url_for("quotes_app.list"))
    # return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
