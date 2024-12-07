from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model for login/signup
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    attendance_rate = db.Column(db.Float, nullable=False)
    study_hours = db.Column(db.Float, nullable=False)
    previous_grade = db.Column(db.Float, nullable=False)
    extracurricular_activities = db.Column(db.Integer, nullable=False)
    parental_support = db.Column(db.String(10), nullable=False)
    final_grade = db.Column(db.Float, nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/loggedin')
def home1():
    return render_template('index1.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Services route
@app.route('/services')
def services():
    return render_template('dashboard.html')


# Add this import at the top of app.py
import pandas as pd


@app.route('/load-csv')
def load_csv():
    try:
        # Read the CSV file
        df = pd.read_csv('student_performance (1).csv')

        # Clear existing data
        Student.query.delete()

        # Insert data from CSV into database
        for _, row in df.iterrows():
            student = Student(
                name=row['Name'],
                gender=row['Gender'],
                attendance_rate=float(row['AttendanceRate']),
                study_hours=float(row['StudyHoursPerWeek']),
                previous_grade=float(row['PreviousGrade']),
                extracurricular_activities=int(row['ExtracurricularActivities']),
                parental_support=row['ParentalSupport'],
                final_grade=float(row['FinalGrade'])
            )
            db.session.add(student)

        db.session.commit()
        return 'Data loaded successfully!'
    except Exception as e:
        db.session.rollback()
        return f'Error loading data: {str(e)}'


# Add this new route to display student data

@app.route('/overview')
def overview():
    try:
        # Fetch all students and calculate statistics
        students = Student.query.all()

        if not students:
            return render_template('overview.html', students=[])

        return render_template('overview.html', students=students)
    except Exception as e:
        flash(f"Error loading overview: {str(e)}", "error")
        return redirect(url_for('dashboard'))
@app.route('/predictor')
def predict():
    return render_template('predictor.html')

# Dashboard route to view and add students
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        student_id = request.form.get('id')
        if student_id:  # Update operation
            student = Student.query.get(student_id)
            if student:
                student.name = request.form['name']
                student.gender = request.form['gender']
                student.attendance_rate = request.form['attendance_rate']
                student.study_hours = request.form['study_hours']
                student.previous_grade = request.form['previous_grade']
                student.extracurricular_activities = request.form['extracurricular_activities']
                student.parental_support = request.form['parental_support']
                student.final_grade = request.form['final_grade']
                db.session.commit()
                flash('Student updated successfully!', 'success')
        else:  # Create operation
            new_student = Student(
                name=request.form['name'],
                gender=request.form['gender'],
                attendance_rate=request.form['attendance_rate'],
                study_hours=request.form['study_hours'],
                previous_grade=request.form['previous_grade'],
                extracurricular_activities=request.form['extracurricular_activities'],
                parental_support=request.form['parental_support'],
                final_grade=request.form['final_grade']
            )
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully!', 'success')
        return redirect(url_for('dashboard'))

    # Fetch all students from the database
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

# Edit student route
@app.route('/dashboard/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get(id)

    if request.method == 'POST':
        # Update student details
        student.name = request.form['name']
        student.gender = request.form['gender']
        student.attendance_rate = request.form['attendance_rate']
        student.study_hours = request.form['study_hours']
        student.previous_grade = request.form['previous_grade']
        student.extracurricular_activities = request.form['extracurricular_activities']
        student.parental_support = request.form['parental_support']
        student.final_grade = request.form['final_grade']

        db.session.commit()  # Commit changes to the database
        flash('Student updated successfully!', 'info')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', student=student)
@app.route('/dashboard/add', methods=['POST'])
def add_student():
    # Get form data
    name = request.form.get('name')
    gender = request.form.get('gender')
    attendance_rate = request.form.get('attendance_rate')
    study_hours = request.form.get('study_hours')
    previous_grade = request.form.get('previous_grade')
    extracurricular_activities = request.form.get('extracurricular_activities')
    parental_support = request.form.get('parental_support')
    final_grade = request.form.get('final_grade')

    # Create a new student object
    new_student = Student(
        name=name,
        gender=gender,
        attendance_rate=attendance_rate,
        study_hours=study_hours,
        previous_grade=previous_grade,
        extracurricular_activities=extracurricular_activities,
        parental_support=parental_support,
        final_grade=final_grade
    )

    # Add student to the database
    db.session.add(new_student)
    db.session.commit()

    # Flash a success message
    flash('Student added successfully!', 'success')

    return redirect(url_for('dashboard'))
# Delete student route
@app.route('/dashboard/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            flash("Login successful!", "success")
            return redirect(url_for('home1'))
        else:
            flash("Invalid credentials. Please try again.", "error")
    return render_template('login.html')

# User signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

# User logout route
@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('userEmail', None)  # Remove user email from session
    session.pop('userPassword', None)  # Remove user password from session
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'userEmail' in session:
        return render_template('home1')  # Render profile page
    else:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

def predict_student_performance(student):
    # Example basic logic
    attendance_weight = 0.3
    study_hours_weight = 0.4
    previous_grade_weight = 0.2
    extracurricular_weight = 0.1

    # Normalize parental support
    parental_support_score = {"High": 1.0, "Medium": 0.5, "Low": 0.2}.get(student['parental_support'], 0.5)

    # Weighted score
    predicted_score = (
        student['attendance_rate'] * attendance_weight +
        student['study_hours'] * study_hours_weight +
        student['previous_grade'] * previous_grade_weight +
        student['extracurricular_activities'] * extracurricular_weight +
        parental_support_score * 10  # Example scaling
    )
    return round(predicted_score, 2)

# Function to get a student by ID
def get_student_by_id(student_id):
    return Student.query.get(student_id)

# Predict Performance

@app.route('/dashboard/predict/<int:student_id>', methods=['POST'])
def predict_performance(student_id):
    student = get_student_by_id(student_id)  # Fetch student details
    if student:  # Check if the student exists
        # Example prediction logic using features from the student object
        predicted_score = predict_student_performance({
            'attendance_rate': student.attendance_rate,
            'study_hours': student.study_hours,
            'previous_grade': student.previous_grade,
            'extracurricular_activities': student.extracurricular_activities,
            'parental_support': student.parental_support
        })

        # Prepare the chart data
        chart_data = {
            "labels": ["Math", "Science", "English", "History", "Art"],
            "data": [random.randint(50, 100) for _ in range(5)]  # Replace this with real data
        }

        # Return the predicted performance and chart data as JSON
        return jsonify({
            'predicted_percentage': predicted_score,
            'chart_data': chart_data
        })
    else:
        flash("Student not found.", "error")
        return redirect(url_for('overview'))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
