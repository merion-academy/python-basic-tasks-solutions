from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import (
    DataRequired,
    EqualTo,
    Length,
    ValidationError,
)

from core.models import User


def unique_username(form, field):
    exists = User.query.filter_by(username=field.raw_data).count()
    if exists:
        raise ValidationError(
            field.gettext("username has to be unique"),
        )


class RegistrationForm(FlaskForm):
    username = fields.StringField(
        label="Username",
        validators=[
            DataRequired(),
            Length(min=3, max=32),
            unique_username,
        ],
    )
    password = fields.PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            Length(min=3),
        ],
    )
    confirm_password = fields.PasswordField(
        label="Confirm Password",
        validators=[
            DataRequired(),
            Length(min=3),
            EqualTo(fieldname="password"),
        ],
    )
    submit = fields.SubmitField(
        label="Register",
    )


class LoginForm(FlaskForm):
    username = fields.StringField(
        label="Username",
        validators=[
            DataRequired(),
        ],
    )
    password = fields.PasswordField(
        label="Password",
        validators=[
            DataRequired(),
        ],
    )
    remember_me = fields.BooleanField(
        label="Remember me",
    )
    submit = fields.SubmitField(
        label="Login",
    )
