from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Flask-Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ofomimatthew7@gmail.com'
app.config['MAIL_PASSWORD'] = 'ctrqvcarhcuibgdy'
mail = Mail(app)

# Set the hardcoded recipient (like in Django's view)
RECIPIENT_EMAIL = 'RaphaelEzema@SignalAllianceTechnology174.onmicrosoft.com'  

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def submit_claim():
    show_modal = False

    if request.method == 'POST':
        try:
            full_name = request.form['full_name']
            email = request.form['email']
            phone = request.form['phone']
            policy_number = request.form['policy_number']
            claim_type = request.form['claim_type']
            incident_date = request.form['incident_date']
            description = request.form['description']
            claim_amount = request.form['claim_amount']
            file = request.files['document']

            filename = ''
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

            # Send email to the hardcoded recipient
            msg = Message('New Insurance Claim Submission',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[RECIPIENT_EMAIL])
            msg.body = f"""
Full Name: {full_name}
Email: {email}
Phone: {phone}
Policy Number: {policy_number}
Claim Type: {claim_type}
Incident Date: {incident_date}
Description: {description}
Claim Amount: {claim_amount}
"""

            if filename:
                with open(filepath, 'rb') as f:
                    msg.attach(filename, file.mimetype, f.read())

            mail.send(msg)
            show_modal = True

        except Exception as e:
            print(f"Error sending email: {e}")

    return render_template('form.html', show_modal=show_modal)
