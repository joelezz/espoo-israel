from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
    name = StringField('Yrityksen nimi ja yhteyshenkilö:', validators=[DataRequired()])
    email = StringField('Sähköposti:', validators=[DataRequired()])
    message = TextAreaField('Viesti:', validators=[DataRequired()])
    submit = SubmitField('Lähetä')
