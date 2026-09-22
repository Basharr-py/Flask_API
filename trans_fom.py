from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class Trans(FlaskForm):
    customer = StringField('Customer', validators=[DataRequired()])
    amount   = StringField ('Amount', validators=[DataRequired()])
    status   = StringField('Status', validators=[DataRequired()])
