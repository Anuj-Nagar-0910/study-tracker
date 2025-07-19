from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'your_super_secret_key' # Needed for flash messages
app.secret_key = os.environ.get('SECRET_KEY', 'default_fallback_key') #For Development Purpose 
# Note: For production, ensure you set SECRET_KEY in Render's environment variables.
db = SQLAlchemy(app)

# Define the Day model
class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_number = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(50), default='Not Started') # Not Started, Completed, Partially Completed, Skipped
    notes = db.Column(db.Text, default='')
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Day {self.day_number}>'

# Create database tables if they don't exist
with app.app_context():
    db.create_all()
    # Populate days if the database is empty
    if Day.query.count() == 0:
        for i in range(1, 31): # Create 30 days
            new_day = Day(day_number=i)
            db.session.add(new_day)
        db.session.commit()

@app.route('/')
def index():
    days = Day.query.order_by(Day.day_number).all()
    return render_template('index.html', days=days)

@app.route('/day/<int:day_num>', methods=['GET', 'POST'])
def day_detail(day_num):
    day = Day.query.filter_by(day_number=day_num).first_or_404()
    if request.method == 'POST':
        day.status = request.form['status']
        day.notes = request.form['notes']
        day.last_updated = datetime.utcnow()
        db.session.commit()
        flash('Day updated successfully!', 'success') # 'success' category for styling
        return redirect(url_for('day_detail', day_num=day_num)) # Redirect back to the same page
    return render_template('day_detail.html', day=day)

if __name__ == '__main__':
    app.run(debug=False)
