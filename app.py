from flask import Flask
from flask_cors import CORS
from models import db, Job
from routes.auth import auth_bp
from routes.job import jobs_bp
from routes.Recruiter import recruiter_bp  

app = Flask(__name__)
app.secret_key = "supersecretkey"

# CORS مع دعم الـ credentials
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recruitment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    if Job.query.count() == 0:
        db.session.add_all([
            Job(title="Frontend Engineer", description="React, TypeScript", city="Cairo", job_type="Full-time"),
            Job(title="Backend Engineer", description="Node, Postgres", city="Remote", job_type="Part-time")
        ])
        db.session.commit()

# تسجيل Blueprints
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(jobs_bp, url_prefix="/api")
app.register_blueprint(recruiter_bp)  

if __name__ == "__main__":
    app.run(debug=True)





