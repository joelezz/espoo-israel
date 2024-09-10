from flask import Flask, request, redirect, url_for, render_template, flash
from flask_mail import Mail, Message
import secrets, os

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER']='daxpower.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lomakkeet@daxpower.com'
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
print(f"EMAIL_PASSWORD: {os.environ.get('EMAIL_PASSWORD')}")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Set a secret key for session management
app.secret_key = secrets.token_hex(16)

# Initialize Flask-Mail
mail = Mail(app)

# Home route to serve the HTML form
@app.route('/')
def home():
    return render_template('index.html')  # Your HTML page with the form

# Route to handle form submission
@app.route('/submit-form', methods=['POST'])
def submit_form():
    # Retrieve form data
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Validate form data
    if not name or not email or not message:
        flash("All fields are required!")
        return redirect(url_for('home'))

    # Send email
    try:
        msg = Message(f"New Contact Form Submission from {name}",
                      sender='lomakkeet@daxpower.com',  # Sender email (your email)
                      recipients=["joe@daxpower.com"])  # Recipient email
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)
        flash("Your message has been sent successfully!")
        return redirect(url_for('thank_you'))
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        flash("Failed to send the message. Please try again later.")
        return redirect(url_for('home'))

# Thank you route
@app.route('/thank-you')
def thank_you():
    return "Thank you for contacting us! We will get back to you shortly."

if __name__ == '__main__':
    app.run()
