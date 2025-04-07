from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email    

class ContactForm(FlaskForm):
    name = StringField('Nimi:', validators=[DataRequired()])
    address = StringField('Postiosoite:', validators=[DataRequired()])
    postal_code = IntegerField('Postinumero:', validators=[DataRequired()])
    city = StringField('Postitoimipaikka:', validators=[DataRequired()])
    email = StringField('Sähköposti:', validators=[DataRequired(), Email()])
    phone = StringField('Puhelin:', validators=[DataRequired()])
    join = SelectField(u"Haluan liittyä Espoon Suomi-Israel yhdistyksen tukijäseneksi:", choices=[("kyllä", "Kyllä"), ("ei", "Ei")], validators=[DataRequired()])
    message = TextAreaField('Viesti:', validators=[DataRequired()])
    accept_policy = BooleanField('Hyväksyn tietosuojaselosteen</a>', validators=[DataRequired()])
    submit = SubmitField('Lähetä')
