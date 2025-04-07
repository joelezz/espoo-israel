import os
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from contact_form import ContactForm
import logging
from logging import FileHandler
from dotenv import load_dotenv



app = Flask(__name__)
csrf = CSRFProtect(app)
load_dotenv()


# Set up logging
if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)


# Flask app config

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '0982730987213iujasdoiased9082u32')

if not app.config['SECRET_KEY'] and not app.debug:
    raise ValueError("No SECRET_KEY set for Flask application in production")
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # ie 1 hour
app.config['SESSION_COOKIE_SECURE'] = True  # Secure cookies (https)
app.config['PREFERRED_URL_SCHEME'] = 'https'  # Ensure the correct scheme for production

app.config['SESSION_TYPE'] = 'filesystem'  # For file-based sessions
app.config['MAIL_SERVER'] = 'send.one.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'moi@espoo-israel.fi'
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['DEBUG'] = False

# session cookie security setting and error handling
if not app.debug:
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    file_handler = FileHandler('error.log')
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

mail = Mail(app)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {e}")
    return render_template('error.html', error=str(e)), 500

@app.route('/', methods=['GET', 'POST'])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        postal_code = form.postal_code.data
        city = form.city.data
        join = form.join.data
        message = form.message.data
        accept_policy = form.accept_policy.data


        # Capture the reCAPTCHA response
        #recaptcha_response = request.form.get('g-recaptcha-response')
        
        """if not recaptcha_response:
            app.logger.warning("No reCAPTCHA response received.")
            flash("Please complete the reCAPTCHA verification.")
            return redirect(url_for('home'))"""


        # Process the form (e.g., send email)
        try:
            msg = Message(f"New Contact Form Submission from {name}",
                          sender='moi@espoo-israel.fi',
                          recipients=["info@espoo-israel.fi", "espoo.israel@gmail.com"])
            msg.body = f"Nimi: {name}\nSähköposti: {email}\nHaluan liittyä jäseneksi: {join}\nOsite: {address}\nPostiosoite: {postal_code}\nPuhelin: {phone}\nHyväksyn ehdot: {accept_policy}\nViestisi: {message}"
            mail.send(msg)
            flash("Message sent successfully!")
            return redirect(url_for('thank_you'))
        except Exception as e:
            app.logger.error(f"Email sending failed: {str(e)}")
            flash("Failed to send message. Please try again later.")
            return redirect(url_for('home'))

    return render_template('index.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f"404 Error: {e}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f"500 Error: {e}")
    return render_template('500.html'), 500



@app.route('/thank_you')  # Match the route name with the redirect
def thank_you():
    return render_template('kiitos.html')
if __name__ == "__main__":
    app.run(debug=True)
