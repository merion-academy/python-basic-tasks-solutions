from flask_login import LoginManager

from core.models import User

login_manager = LoginManager()

login_manager.login_view = "auth_app.login"

login_manager.login_message = "Please login to use this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id) -> User | None:
    return User.query.get(user_id)
