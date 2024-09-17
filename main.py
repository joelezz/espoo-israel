from flask import Flask, request, redirect, url_for, render_template, flash
from flask_mail import Mail, Message
import secrets, os
#from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from contact_form import ContactForm

app = Flask(__name__)
csrf = CSRFProtect(app)
#load_dotenv()

# The secret key for session management
app.secret_key = os.environ.get('SECRET_KEY')
# Flask-Mail configurations
app.config['MAIL_SERVER'] = 'smtp.daxpower.com'  # Ensure this is the correct SMTP server
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lomakkeet@daxpower.com'
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SECRET_KEY'] = app.secret_key

# Initialize Flask-Mail
mail = Mail(app)

@app.before_request
def log_request_info():
    if request.method == "POST":
        print("POST request received")
        print(f"CSRF Token: {request.form.get('csrf_token')}")


# Home route to serve the HTML one pager and form
@app.route('/', methods=['GET', 'POST'])
def home():
    form = ContactForm()  # Your custom form
    if form.validate_on_submit():
        # Retrieve form data
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # Send email
        try:
            msg = Message(f"New Contact Form Submission from {name}",
                          sender='lomakkeet@daxpower.com',  # Sender email
                          recipients=["zzjoe@tuta.io"])  # Recipient email
            msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            mail.send(msg)
            flash("Viestisi lähetettiin onnistuneesti!")
            return redirect(url_for('thank_you'))
        except Exception as e:
            print(f"Viestin toimitus ei onnistunut: {str(e)}")
            flash("Viestin toimitus ei onnistunut, kokeile uudestaan hetken kuluttua.")
            return redirect(url_for('home'))

    return render_template('index.html', form=form)

# Thank you route
@app.route('/kiitos')
def thank_you():
    return "Kiitos yhteydenotosta! Palaamme sinulle mahdollisimman pian."

if __name__ == '__main__':
    app.run()  