from flask import Blueprint, request, jsonify
from models import db, Application, Job
from services.email_service import send_email
from config import RECRUITER_EMAIL

applications_bp = Blueprint("applications", __name__, url_prefix="/api/applications")

@applications_bp.route("/", methods=["POST"])
def apply_job():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    job_id = data.get("job_id")

    if not name or not email or not job_id:
        return jsonify({"error": "name, email, job_id required"}), 400

    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    app_obj = Application(applicant_name=name, email=email, job_id=job_id)
    db.session.add(app_obj)
    db.session.commit()

    # Notifications
    send_email(email, "Application Received", f"Hi {name}, your application for {job.title} was received.")
    send_email(RECRUITER_EMAIL, "New Job Application", f"New application from {name} for {job.title}.")

    return jsonify({"message": "Application submitted"}), 201
