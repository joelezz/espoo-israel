from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

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

    # Process the form data
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Message: {message}")

    return redirect(url_for('thank_you'))

# Route for form submission error
@app.route('/form-error')
def form_error():
    return "Form submission error. Please fill out all fields."

# Thank you route
@app.route('/thank-you')
def thank_you():
    return "Thank you for contacting us! We will get back to you shortly."

if __name__ == '__main__':
    app.run(debug=True)