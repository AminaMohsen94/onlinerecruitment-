from flask import Flask, jsonify, request
from flask_cors import CORS
import smtplib
from email.message import EmailMessage

from models import db, Job, Application   # ✅ import models

# =====================
# App config
# =====================
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recruitment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)   # ✅ init db with app

# =====================
# Email config
# =====================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"      # غيريها
EMAIL_PASSWORD = "your_app_password"       # App Password
RECRUITER_EMAIL = "recruiter@gmail.com"

def send_email(to, subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

# =====================
# Create DB + Sample Data
# =====================
with app.app_context():
    db.create_all()

    if Job.query.count() == 0:
        db.session.add_all([
            Job(
                title='Frontend Engineer',
                description='React, TypeScript',
                city='Cairo',
                job_type='Full-time'
            ),
            Job(
                title='Backend Engineer',
                description='Node, Postgres',
                city='Remote',
                job_type='Part-time'
            )
        ])
        db.session.commit()

# =====================
# API Routes
# =====================

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([
        {
            "id": j.id,
            "title": j.title,
            "description": j.description,
            "city": j.city,
            "type": j.job_type
        }
        for j in jobs
    ])

@app.route('/api/apply', methods=['POST'])
def apply_job():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get("name")
    email = data.get("email")
    job_id = data.get("job_id")

    if not name or not email or not job_id:
        return jsonify({"error": "name, email, job_id required"}), 400

    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    application = Application(
        applicant_name=name,
        email=email,
        job_id=job_id
    )

    db.session.add(application)
    db.session.commit()

    # =====================
    # Notifications
    # =====================

    send_email(
        email,
        "Application Received",
        f"Hi {name},\n\nYour application for {job.title} was received."
    )

    send_email(
        RECRUITER_EMAIL,
        "New Job Application",
        f"New application from {name} for {job.title}."
    )

    return jsonify({"message": "Application submitted successfully"}), 201

# =====================
# Run App
# =====================
if __name__ == "__main__":
    app.run(debug=True)


