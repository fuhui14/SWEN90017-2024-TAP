from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transcription(db.Model):
    __tablename__ = 'transcriptions'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String(120), unique=True, nullable=False)
    file_name = db.Column(db.String(120), nullable=False)
    transcription_text = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Processing")
    created_at = db.Column(db.DateTime, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
