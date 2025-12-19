from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# =====================
# Job Model
# =====================

class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)

    applications = db.relationship(
        'Application',
        backref='job',
        lazy=True,
        cascade="all, delete-orphan"
    )

# =====================
# Application Model
# =====================

class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    applicant_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    cv = db.Column(db.String(200))  # path to CV file
    status = db.Column(
        db.String(20),
        default='pending'
    )  # pending / shortlisted / rejected / accepted

    notes = db.Column(db.Text, nullable=True)

    job_id = db.Column(
        db.Integer,
        db.ForeignKey('job.id'),
        nullable=False
    )

