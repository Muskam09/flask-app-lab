from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SelectField, SubmitField,
    BooleanField, DateTimeLocalField
)
from wtforms.validators import DataRequired, Length, Optional

class PostForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(), 
        Length(min=5, max=150)
    ])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('news', 'News'),
        ('publication', 'Publication'),
        ('tech', 'Technology'),
        ('other', 'Other')
    ], validators=[DataRequired()])


    publish_date = DateTimeLocalField(
        'Publication Date',
        format='%Y-%m-%dT%H:%M',
        validators=[Optional()]
    )
    enabled = BooleanField('Enabled (is_active)', default=True)

    submit = SubmitField('Submit')

# Порожня форма для CSRF
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')