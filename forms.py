from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired

class ExpenseForm(FlaskForm):
    name = StringField('nazwa', validators=[DataRequired()])
    amount = FloatField('wartość', validators=[DataRequired()])