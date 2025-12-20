from flask import Blueprint, request, jsonify
from models import db, Job, Application

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([
        {
            "id": j.id,
            "title": j.title,
            "description": j.description,
            "city": j.city,
            "type": j.job_type
        } for j in jobs
    ])

@jobs_bp.route("/apply", methods=["POST"])
def apply_job():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get("name")
    email = data.get("email")
    job_id = data.get("job_id")

    if not name or not email or not job_id:
        return jsonify({"error": "Missing fields"}), 400

    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    app = Application(
        applicant_name=name,
        email=email,
        job_id=job_id
    )
    db.session.add(app)
    db.session.commit()

    return jsonify({"message": "Application submitted successfully"}), 201

