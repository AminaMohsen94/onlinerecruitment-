from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
from models import db, Job, Application
import os

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')

# Post a Job
@recruiter_bp.route('/job/new', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        job = Job(title=title, description=description)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('recruiter.view_jobs'))
    return render_template('post_job.html')

# Edit Job
@recruiter_bp.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        job.title = request.form['title']
        job.description = request.form['description']
        db.session.commit()
        return redirect(url_for('recruiter.view_jobs'))
    return render_template('edit_job.html', job=job)

# Delete Job
@recruiter_bp.route('/job/<int:job_id>/delete', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('recruiter.view_jobs'))

# View all Jobs
@recruiter_bp.route('/jobs')
def view_jobs():
    jobs = Job.query.all()
    return render_template('recruiter_jobs.html', jobs=jobs)

# View Applicants for a Job
@recruiter_bp.route('/job/<int:job_id>/applications')
def view_applicants(job_id):
    applications = Application.query.filter_by(job_id=job_id).all()
    return render_template('recruiter_applicants.html', applications=applications)

# Download CV
@recruiter_bp.route('/application/<int:app_id>/download')
def download_cv(app_id):
    app = Application.query.get_or_404(app_id)
    directory = os.path.dirname(app.cv)
    filename = os.path.basename(app.cv)
    return send_from_directory(directory, filename, as_attachment=True)

# Update Application Status & Notes
@recruiter_bp.route('/application/<int:app_id>/update', methods=['POST'])
def update_application(app_id):
    app = Application.query.get_or_404(app_id)
    app.status = request.form.get('status', app.status)
    app.notes = request.form.get('notes', app.notes)
    db.session.commit()
    return redirect(request.referrer or url_for('recruiter.view_jobs'))
