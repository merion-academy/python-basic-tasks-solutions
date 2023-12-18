from flask_wtf import FlaskForm
from wtforms import fields, validators


class CategoryForm(FlaskForm):
    name = fields.StringField(
        label="Category name",
        validators=[
            validators.DataRequired(),
            validators.Length(min=3),
        ],
    )
    description = fields.TextAreaField(
        label="Category description",
        validators=[
            validators.DataRequired(),
            validators.Length(min=10),
        ],
    )
    submit = fields.SubmitField(
        "Create",
    )
