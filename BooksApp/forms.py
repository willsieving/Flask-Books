from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    cover = FileField('Upload Book Cover', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')


class UpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    cover = FileField('Update Book Cover', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')