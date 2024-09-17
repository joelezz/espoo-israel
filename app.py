import os
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from contact_form import ContactForm
import logging
from logging import FileHandler

app = Flask(__name__)
csrf = CSRFProtect(app)

# Load environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.daxpower.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lomakkeet@daxpower.com'
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Set up logging
if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {e}")
    return "An internal error occurred.", 500

@app.route('/', methods=['GET', 'POST'])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        try:
            msg = Message(f"New Contact Form Submission from {name}",
                          sender='lomakkeet@daxpower.com',
                          recipients=["zzjoe@tuta.io"])
            msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            mail.send(msg)
            flash("Viestisi lähetettiin onnistuneesti!")
            return redirect(url_for('thank_you'))
        except Exception as e:
            app.logger.error(f"Email sending failed: {str(e)}")
            flash("Viestin toimitus ei onnistunut, kokeile uudestaan hetken kuluttua.")
            return redirect(url_for('home'))

    return render_template('index.html', form=form)

@app.route('/kiitos')
def thank_you():
    return "Kiitos yhteydenotosta! Palaamme sinulle mahdollisimman pian."

if __name__ == '__main__':
    app.run()
