from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recruitment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =====================
# Models
# =====================

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    job = db.relationship('Job', backref='applications')


# =====================
# Create DB + Sample Data
# =====================

with app.app_context():
    db.create_all()

    if Job.query.count() == 0:
        jobs = [
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
        ]
        db.session.add_all(jobs)
        db.session.commit()


# =====================
# API Routes
# =====================

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
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


@app.route('/api/apply', methods=['POST'])
def apply_job():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    name = data.get('name')
    job_id = data.get('job_id')

    if not name or not job_id:
        return jsonify({'error': 'name and job_id are required'}), 400

    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    application = Application(name=name, job_id=job_id)
    db.session.add(application)
    db.session.commit()

    return jsonify({'message': 'Application submitted successfully'}), 201


# =====================
# Run App
# =====================

if __name__ == '__main__':
    app.run(debug=True)

