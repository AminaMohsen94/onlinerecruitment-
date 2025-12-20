from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Job, Application

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')

@recruiter_bp.route('/jobs')
def view_jobs():
    jobs = Job.query.all()
    return render_template('recruiter_jobs.html', jobs=jobs)

@recruiter_bp.route('/job/new', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        city = request.form.get('city', 'Remote')
        job_type = request.form.get('job_type', 'Full-time')
        job = Job(title=title, description=description, city=city, job_type=job_type)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('recruiter.view_jobs'))
    return render_template('post_job.html')

@recruiter_bp.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        job.title = request.form['title']
        job.description = request.form['description']
        job.city = request.form['city']
        job.job_type = request.form['job_type']
        db.session.commit()
        return redirect(url_for('recruiter.view_jobs'))
    return render_template('edit_job.html', job=job)

@recruiter_bp.route('/job/<int:job_id>/delete', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('recruiter.view_jobs'))

@recruiter_bp.route('/job/<int:job_id>/applications')
def view_applicants(job_id):
    applications = Application.query.filter_by(job_id=job_id).all()
    return render_template('recruiter_applicants.html', applications=applications)

