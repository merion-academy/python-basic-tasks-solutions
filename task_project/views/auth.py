import logging
from http import HTTPStatus

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    Blueprint,
    request,
)
from flask_login import (
    login_user,
    current_user,
    login_required,
    logout_user,
)
from sqlalchemy.exc import DatabaseError
from werkzeug.exceptions import InternalServerError

from core.helpers import is_safe_url
from core.models import db, User
from views.forms.auth import RegistrationForm, LoginForm

log = logging.getLogger(__name__)

auth_app = Blueprint("auth_app", __name__)


@auth_app.route(
    "/register/",
    methods=["GET", "POST"],
    endpoint="register",
)
def register():
    if current_user.is_authenticated:
        # Redirect user to some other page if already logged in
        return redirect(url_for("index"))

    form = RegistrationForm()

    if request.method == "GET":
        return render_template(
            "auth/register.html",
            form=form,
        )

    if not form.validate_on_submit():
        return (
            render_template(
                "auth/register.html",
                form=form,
            ),
            HTTPStatus.BAD_REQUEST,
        )

    user = User(username=form.username.data)
    user.set_password(form.password.data)
    db.session.add(user)
    try:
        db.session.commit()
    except DatabaseError:
        log.exception("error saving user %r", user.username)
        raise InternalServerError("Could not save user! Something is wrong")

    login_user(user)  # Logs in the user after successful registration
    flash(f"Welcome, {user.username}!", "success")
    return redirect(url_for("index"))


@auth_app.route(
    "/login/",
    methods=["GET", "POST"],
    endpoint="login",
)
def login():
    if current_user.is_authenticated:
        # Redirect user to some other page if already logged in
        return redirect(url_for("index"))

    form = LoginForm()

    if request.method == "GET":
        return render_template(
            "auth/login.html",
            form=form,
        )

    if not form.validate_on_submit():
        return (
            render_template(
                "auth/login.html",
                form=form,
            ),
            HTTPStatus.BAD_REQUEST,
        )

    user = (
        # find user
        User.query
        # filter or filter_by
        .filter_by(
            # search by username
            username=form.username.data,
        ).one_or_none()
    )

    if not (user and user.check_password(form.password.data)):
        flash("Invalid username or password", "danger")
        return redirect(url_for("auth_app.login"))

    next_url = request.args.get("next")
    # you have to check if the url is safe for redirects,
    # meaning it matches the request host.
    # See Django's url_has_allowed_host_and_scheme for an example.
    if not is_safe_url(request.host, next_url):
        next_url = url_for("index")

    login_user(user, remember=form.remember_me.data)
    flash("Logged in successfully!", "success")
    return redirect(next_url)


@auth_app.get("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    flash("See you later!", "info")
    return redirect(url_for("index"))
