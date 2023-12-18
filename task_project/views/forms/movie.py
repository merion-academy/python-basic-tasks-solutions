from flask_wtf import FlaskForm
from wtforms import fields, validators

from core.models import Category


def get_categories_choices():
    return [
        # value, label
        (str(c.id), c.name)
        # apply ordering
        for c in Category.query.order_by(Category.name).all()
    ]


class MovieForm(FlaskForm):
    title = fields.StringField(
        label="Movie Title",
        validators=[
            validators.DataRequired(),
            validators.Length(min=3),
        ],
    )
    year = fields.IntegerField(
        label="Release year",
        validators=[
            validators.DataRequired(),
            validators.NumberRange(min=1888),
        ],
    )
    category = fields.SelectField(
        label="Category",
        validators=[validators.DataRequired()],
        choices=get_categories_choices,
    )
    submit = fields.SubmitField(
        "Create",
    )
