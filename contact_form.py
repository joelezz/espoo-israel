from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email    
from flask_wtf.recaptcha import RecaptchaField



class ContactForm(FlaskForm):
    name = StringField('Nimi:', validators=[DataRequired()])
    email = StringField('Sähköposti:', validators=[DataRequired(), Email()])
    phone = StringField('Puhelin:', validators=[DataRequired()])
    join = SelectField(u"Haluan liittyä Espoon Suomi-Israel yhdistyksen tukijäseneksi:", choices=[("kyllä", "Kyllä"), ("ei", "Ei")], validators=[DataRequired()])
    message = TextAreaField('Viesti:', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Lähetä')
