# database.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_number = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(50), default='Not Started') # e.g., 'Not Started', 'Completed', 'Partially Completed', 'Skipped'
    notes = db.Column(db.Text, default='')
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Day {self.day_number} - Status: {self.status}>"

def create_db(app):
    with app.app_context():
        db.create_all()

def initialize_days(app, num_days=30):
    with app.app_context():
        # Check if days already exist to prevent re-creation on every run
        if Day.query.count() == 0:
            for i in range(1, num_days + 1):
                new_day = Day(day_number=i)
                db.session.add(new_day)
            db.session.commit()
            print(f"Initialized {num_days} study days.")
        else:
            print("Study days already initialized.")