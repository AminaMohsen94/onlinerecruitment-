from flask import Blueprint, request, jsonify
from models import Job, Application

search_bp = Blueprint("search", __name__, url_prefix="/api/search")

@search_bp.route("/jobs", methods=["GET"])
def search_jobs():
    q = request.args.get("q", "").lower()
    jobs = Job.query.filter(
        Job.title.ilike(f"%{q}%") |
        Job.description.ilike(f"%{q}%") |
        Job.city.ilike(f"%{q}%") |
        Job.job_type.ilike(f"%{q}%")
    ).all()
    return jsonify([
        {"id": j.id, "title": j.title, "description": j.description, "city": j.city, "type": j.job_type}
        for j in jobs
    ])

@search_bp.route("/candidates", methods=["GET"])
def search_candidates():
    q = request.args.get("q", "").lower()
    applications = Application.query.filter(Application.applicant_name.ilike(f"%{q}%")).all()
    return jsonify([
        {"id": a.id, "name": a.applicant_name, "job": a.job.title} for a in applications
    ])

