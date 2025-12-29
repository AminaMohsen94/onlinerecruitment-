import os

SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")


SQLALCHEMY_DATABASE_URI = "sqlite:///recruitment.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  
RECRUITER_EMAIL = "recruiter@gmail.com"
