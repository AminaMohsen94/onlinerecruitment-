from flask import Blueprint, request, jsonify
from models import Job, Application

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search/jobs', methods=['GET'])
def search_jobs():
    q = request.args.get('q', '').lower()

    jobs = Job.query.filter(
        Job.title.ilike(f'%{q}%') |
        Job.description.ilike(f'%{q}%') |
        Job.city.ilike(f'%{q}%') |
        Job.job_type.ilike(f'%{q}%')
    ).all()

    return jsonify([
        {
            'id': j.id,
            'title': j.title,
            'description': j.description,
            'city': j.city,
            'type': j.job_type
        }
        for j in jobs
    ])



@search_bp.route('/api/search/candidates', methods=['GET'])
def search_candidates():
    q = request.args.get('q', '').lower()

    applications = Application.query.filter(
        Application.name.ilike(f'%{q}%')
    ).all()

    return jsonify([
        {
            'id': a.id,
            'name': a.name,
            'job': a.job.title
        }
        for a in applications
    ])
