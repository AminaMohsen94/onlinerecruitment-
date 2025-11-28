from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recruitment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# Create DB
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Database ready"

if __name__ == "__main__":
    app.run(debug=True)
