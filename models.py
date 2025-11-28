from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    applications = db.relationship('Application', backref='job', lazy=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_name = db.Column(db.String(100), nullable=False)
    cv = db.Column(db.String(200))  # path to CV file
    status = db.Column(db.String(20), default='pending')  # pending / shortlisted / rejected / accepted
    notes = db.Column(db.Text, nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
