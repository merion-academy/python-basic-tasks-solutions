from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import StringField


class QuoteForm(FlaskForm):
    text = StringField(
        label="Quote text",
        validators=[
            validators.DataRequired(),
            validators.Length(min=3),
        ],
    )
