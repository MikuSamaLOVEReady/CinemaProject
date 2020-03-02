from flask_wtf import Form, FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SelectField, IntegerField, PasswordField, SubmitField, \
    FileField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from app.models import Tag


def tag_query():
    return Tag.query


class UploadForm(FlaskForm):
    FilmName = StringField('FilmName', validators=[DataRequired()])
    Blurb = StringField('Blurb', validators=[DataRequired()])
    Certificate = StringField('Certificate', validators=[DataRequired()])
    Director = StringField('Director', validators=[DataRequired()])
    LeadActors = StringField('LeadActors', validators=[DataRequired()])
    FilmLength = StringField('FilmLength', validators=[DataRequired()])
    Genre = QuerySelectMultipleField('Genre', query_factory=tag_query, get_label='name', allow_blank=True)
    Ranking = IntegerField('Ranking', validators=[DataRequired()], default=100)
    file = FileField('File')


class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])


class TimeForm(FlaskForm):
    Date = DateField('Date', validators=[DataRequired()])


class FilmScheduleForm(Form):
    Room = StringField('Room', validators=[DataRequired()])
    Date = DateField('Date', validators=[DataRequired()])
    Time = StringField('Time', validators=[DataRequired()])
    Price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')
