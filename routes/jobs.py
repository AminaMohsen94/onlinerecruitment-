from flask import Blueprint, jsonify, request
from models import db, Job

jobs_bp = Blueprint("jobs", __name__, url_prefix="/api/jobs")

@jobs_bp.route("/", methods=["GET"])
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

@jobs_bp.route("/", methods=["POST"])
def create_job():
    data = request.get_json()
    job = Job(
        title=data["title"],
        description=data["description"],
        city=data["city"],
        job_type=data["job_type"]
    )
    db.session.add(job)
    db.session.commit()
    return jsonify({"message": "Job created"}), 201
