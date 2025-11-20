from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SelectField, SubmitField,
    BooleanField, DateTimeLocalField, SelectMultipleField
)
from wtforms.validators import DataRequired, Length, Optional
from app import db
from app.users.models import User
from app.posts.models import Tag

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
    author_id = SelectField("Author", coerce=int, validators=[DataRequired()])

    tags = SelectMultipleField("Tags", coerce=int)

    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        stmt_users = db.select(User).order_by(User.username)
        self.author_id.choices = [
            (user.id, user.username) for user in db.session.scalars(stmt_users).all()
        ]

        stmt_tags = db.select(Tag).order_by(Tag.name)
        self.tags.choices = [
            (tag.id, tag.name) for tag in db.session.scalars(stmt_tags).all()
        ]

# Порожня форма для CSRF
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')