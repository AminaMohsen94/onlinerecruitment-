from fastapi import FastAPI, UploadFile, File, Form, Depends
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.sql import func
import os
import shutil

app = FastAPI()

# ================= DATABASE =================
DATABASE_URL = "sqlite:///./applications.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ================= MODEL =================
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)   # from Auth API
    job_id = Column(Integer, nullable=False)    # from Jobs API
    cv_file = Column(String, nullable=True)
    status = Column(String, default="draft")    # draft / submitted
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

Base.metadata.create_all(bind=engine)

# ================= UPLOAD =================
UPLOAD_DIR = "uploads/cv"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ================= DEPENDENCY =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= ROUTES =================

# Create application draft
@app.post("/applications/draft")
def create_application(
    user_id: int = Form(...),
    job_id: int = Form(...),
    db: Session = Depends(get_db)
):
    application = Application(user_id=user_id, job_id=job_id, status="draft")
    db.add(application)
    db.commit()
    db.refresh(application)
    return {"message": "Application draft created", "application_id": application.id}

# Upload CV
@app.post("/applications/{app_id}/upload-cv")
def upload_cv(app_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        return {"error": "Application not found"}

    filename = file.filename.replace(" ", "_")
    file_path = os.path.join(UPLOAD_DIR, f"{app_id}_{filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    application.cv_file = file_path
    db.commit()
    return {"message": "CV uploaded successfully"}

# Submit application
@app.post("/applications/{app_id}/submit")
def submit_application(app_id: int, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        return {"error": "Application not found"}
    if not application.cv_file:
        return {"error": "Upload CV before submitting"}

    application.status = "submitted"
    db.commit()
    return {"message": "Application submitted"}
