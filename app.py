from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
from werkzeug.utils import secure_filename
from datetime import datetime

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

# Set the hardcoded recipient
# 'RaphaelEzema@SignalAllianceTechnology174.onmicrosoft.com' 
# 'rezema@saconsulting.ai'
RECIPIENT_EMAIL = 'rezema@saconsulting.ai'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_html_table(data):
    html = """
    <html>
        <head>
            <style>
                body { 
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }
                .claim-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }
                .claim-table th {
                    background-color: #4361ee;
                    color: white;
                    text-align: left;
                    padding: 12px;
                    border: 1px solid #ddd;
                }
                .claim-table td {
                    padding: 12px;
                    border: 1px solid #ddd;
                }
                .claim-table tr:nth-child(even) {
                    background-color: #f8f9fa;
                }
                .claim-table tr:hover {
                    background-color: #f1f1f1;
                }
                .section-header {
                    background-color: #3a0ca3 !important;
                    color: white !important;
                    font-weight: bold;
                    text-transform: uppercase;
                }
                h2 {
                    color: #4361ee;
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <h2>New Insurance Claim Submission</h2>
    """
    
    # Prepare all data with defaults for optional fields
    formatted_data = {
        **data,
        'police_report_number': data.get('police_report_number', 'N/A'),
        'witness_information': data.get('witness_information', 'N/A'),
        'repair_estimates': data.get('repair_estimates', 'N/A'),
        'medical_details': data.get('medical_details', 'N/A'),
        'swift_code': data.get('swift_code', 'N/A'),
        'claimant_name': data.get('claimant_name', 'N/A'),
        'claimant_relationship': data.get('claimant_relationship', 'N/A'),
        'claimant_contact': data.get('claimant_contact', 'N/A')
    }

    # Policyholder Information
    html += """
            <table class="claim-table">
                <tr><th colspan="2" class="section-header">Policyholder Information</th></tr>
                <tr><td><strong>Full Name</strong></td><td>{policyholder_name}</td></tr>
                <tr><td><strong>Policy Number</strong></td><td>{policy_number}</td></tr>
                <tr><td><strong>Address</strong></td><td>{policyholder_address}</td></tr>
                <tr><td><strong>Phone Number</strong></td><td>{policyholder_phone}</td></tr>
                <tr><td><strong>Email Address</strong></td><td>{policyholder_email}</td></tr>
                <tr><td><strong>Date of Birth</strong></td><td>{policyholder_dob}</td></tr>
            </table>
    """.format(**formatted_data)
    
    # Claimant Information (if different)
    if data['claimant_different'] == 'yes':
        html += """
            <table class="claim-table">
                <tr><th colspan="2" class="section-header">Claimant Information</th></tr>
                <tr><td><strong>Full Name</strong></td><td>{claimant_name}</td></tr>
                <tr><td><strong>Relationship to Policyholder</strong></td><td>{claimant_relationship}</td></tr>
                <tr><td><strong>Contact Information</strong></td><td>{claimant_contact}</td></tr>
            </table>
        """.format(**formatted_data)
    
    # Claim Information
    html += """
            <table class="claim-table">
                <tr><th colspan="2" class="section-header">Claim Information</th></tr>
                <tr><td><strong>Nature of Claim</strong></td><td>{nature_of_claim}</td></tr>
                <tr><td><strong>Incident Type</strong></td><td>{incident_type}</td></tr>
            </table>
    """.format(**formatted_data)
    
    # Incident Details
    html += """
            <table class="claim-table">
                <tr><th colspan="2" class="section-header">Incident Details</th></tr>
                <tr><td><strong>Date of Incident</strong></td><td>{incident_date}</td></tr>
                <tr><td><strong>Time of Incident</strong></td><td>{incident_time}</td></tr>
                <tr><td><strong>Location of Incident</strong></td><td>{incident_location}</td></tr>
                <tr><td><strong>Description of Incident</strong></td><td>{incident_description}</td></tr>
                <tr><td><strong>Cause of Loss/Damage</strong></td><td>{cause_of_loss}</td></tr>
                <tr><td><strong>Police Report Number</strong></td><td>{police_report_number}</td></tr>
                <tr><td><strong>Witness Information</strong></td><td>{witness_information}</td></tr>
            </table>
    """.format(**formatted_data)
    
    # Loss and Damage
    html += """
            <table class="claim-table">
                <tr><th colspan="2" class="section-header">Loss and Damage</th></tr>
                <tr><td><strong>Description of Items</strong></td><td>{loss_description}</td></tr>
                <tr><td><strong>Estimated Value</strong></td><td>{estimated_value}</td></tr>
                <tr><td><strong>Repair Estimates</strong></td><td>{repair_estimates}</td></tr>
                <tr><td><strong>Medical Details</strong></td><td>{medical_details}</td></tr>
            </table>
    """.format(**formatted_data)
    
    # Bank Details
    html += """
            <table class="claim-table">
                <tr><th colspan="2" class="section-header">Bank Details for Payout</th></tr>
                <tr><td><strong>Account Name</strong></td><td>{account_name}</td></tr>
                <tr><td><strong>Bank Name</strong></td><td>{bank_name}</td></tr>
                <tr><td><strong>Account Number</strong></td><td>{account_number}</td></tr>
                <tr><td><strong>Bank Branch</strong></td><td>{bank_branch}</td></tr>
                <tr><td><strong>Swift Code</strong></td><td>{swift_code}</td></tr>
            </table>
    """.format(**formatted_data)
    
    # Supporting Documents
    if data['filenames']:
        html += """
            <table class="claim-table">
                <tr><th class="section-header">Supporting Documents</th></tr>
        """
        for filename in data['filenames']:
            html += f"<tr><td>{filename}</td></tr>"
        html += "</table>"
    
    html += """
        </body>
    </html>
    """
    
    return html

@app.route('/', methods=['GET', 'POST'])
def submit_claim():
    show_modal = False

    if request.method == 'POST':
        try:
            # Policyholder Information
            policyholder_name = request.form['policyholder_name']
            policy_number = request.form['policy_number']
            policyholder_address = request.form['policyholder_address']
            policyholder_phone = request.form['policyholder_phone']
            policyholder_email = request.form['policyholder_email']
            policyholder_dob = request.form['policyholder_dob']
            
            # Claimant Information
            claimant_different = request.form.get('claimant_different', 'no')
            claimant_name = request.form.get('claimant_name', '')
            claimant_relationship = request.form.get('claimant_relationship', '')
            claimant_contact = request.form.get('claimant_contact', '')
            
            # Claim Information
            nature_of_claim = request.form['nature_of_claim']
            incident_type = request.form['incident_type']
            
            # Incident Details
            incident_date = request.form['incident_date']
            incident_time = request.form['incident_time']
            incident_location = request.form['incident_location']
            incident_description = request.form['incident_description']
            cause_of_loss = request.form['cause_of_loss']
            police_report_number = request.form.get('police_report_number', '')
            witness_information = request.form.get('witness_information', '')
            
            # Loss and Damage
            loss_description = request.form['loss_description']
            estimated_value = request.form['estimated_value']
            repair_estimates = request.form.get('repair_estimates', '')
            medical_details = request.form.get('medical_details', '')
            
            # Bank Details
            account_name = request.form['account_name']
            bank_name = request.form['bank_name']
            account_number = request.form['account_number']
            bank_branch = request.form['bank_branch']
            swift_code = request.form.get('swift_code', '')
            
            # Handle file uploads
            uploaded_files = request.files.getlist('documents')
            filenames = []
            
            for file in uploaded_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    filenames.append(filename)

            # Prepare data for email
            data = {
                'policyholder_name': policyholder_name,
                'policy_number': policy_number,
                'policyholder_address': policyholder_address,
                'policyholder_phone': policyholder_phone,
                'policyholder_email': policyholder_email,
                'policyholder_dob': policyholder_dob,
                'claimant_different': claimant_different,
                'claimant_name': claimant_name,
                'claimant_relationship': claimant_relationship,
                'claimant_contact': claimant_contact,
                'nature_of_claim': nature_of_claim,
                'incident_type': incident_type,
                'incident_date': incident_date,
                'incident_time': incident_time,
                'incident_location': incident_location,
                'incident_description': incident_description,
                'cause_of_loss': cause_of_loss,
                'police_report_number': police_report_number,
                'witness_information': witness_information,
                'loss_description': loss_description,
                'estimated_value': estimated_value,
                'repair_estimates': repair_estimates,
                'medical_details': medical_details,
                'account_name': account_name,
                'bank_name': bank_name,
                'account_number': account_number,
                'bank_branch': bank_branch,
                'swift_code': swift_code,
                'filenames': filenames
            }

            # Send email with HTML table
            msg = Message('New Insurance Claim Submission',
                         sender=app.config['MAIL_USERNAME'],
                         recipients=[RECIPIENT_EMAIL])
            
            msg.html = generate_html_table(data)
            
            # Attach files
            for filename in filenames:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                with open(filepath, 'rb') as f:
                    msg.attach(filename, 'application/octet-stream', f.read())

            mail.send(msg)
            show_modal = True

        except Exception as e:
            print(f"Error processing claim: {e}")

    return render_template('form.html', show_modal=show_modal)

if __name__ == '__main__':
    app.run(debug=True, port=5000)