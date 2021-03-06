from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class FetchRecordsForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    write2db = BooleanField('Write to PostgreSQL')
    submit = SubmitField('Get Data')
