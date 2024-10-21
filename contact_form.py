from flask_wtf import FlaskForm
<<<<<<< HEAD
from wtforms import StringField, SelectField, TextAreaField, SubmitField, IntegerField, widgets, BooleanField
=======
from wtforms import StringField, SelectField, TextAreaField, SubmitField
>>>>>>> efedbc1 (Preparing deployment to heroku)
from wtforms.validators import DataRequired, Email    
from flask_wtf.recaptcha import RecaptchaField



class ContactForm(FlaskForm):
    name = StringField('Nimi:', validators=[DataRequired()])
<<<<<<< HEAD
    address = StringField('Postiosoite:', validators=[DataRequired()])
    postal_code = IntegerField('Postinumero:', validators=[DataRequired()])
    city = StringField('Postitoimipaikka:', validators=[DataRequired()])
    email = StringField('Sähköposti:', validators=[DataRequired(), Email()])
    phone = StringField('Puhelin:', validators=[DataRequired()])
    join = SelectField(u"Haluan liittyä Espoon Suomi-Israel yhdistyksen jäseneksi:", choices=[("kyllä", "Kyllä"), ("ei", "Ei")], validators=[DataRequired()])
    message = TextAreaField('Viesti:', validators=[DataRequired()])
    accept_policy = BooleanField('Hyväksyn tietosuojaselosteen</a>', validators=[DataRequired()])
=======
    email = StringField('Sähköposti:', validators=[DataRequired(), Email()])
    phone = StringField('Puhelin:', validators=[DataRequired()])
    join = SelectField(u"Haluan liittyä Espoon Suomi-Israel yhdistyksen tukijäseneksi:", choices=[("kyllä", "Kyllä"), ("ei", "Ei")], validators=[DataRequired()])
    message = TextAreaField('Viesti:', validators=[DataRequired()])
>>>>>>> efedbc1 (Preparing deployment to heroku)
    recaptcha = RecaptchaField()
    submit = SubmitField('Lähetä')
