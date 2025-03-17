from flask import Flask,render_template,request,redirect,url_for,session
import db
from config import Config  # Import Config class
import json
from datetime import timedelta

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY  # Set the secret key from Config

@app.route('/')
def home():
    # Get all subjects for the dropdown menu
    subjects = db.query("SELECT * FROM subject ORDER BY name")
    return render_template('home.html', subjects=subjects)

@app.route('/asignatura')
def asignatura_redirect():
    # Redirect to the home page if no subject ID is provided
    return redirect(url_for('home'))

@app.route('/asignatura/<int:subject_id>')
def asignatura(subject_id):
    # Get subject information
    subject = db.query_one("SELECT * FROM subject WHERE subject_id = %s", (subject_id,))
    if not subject:
        return "Asignatura no encontrada", 404
    
    # Get students enrolled in this subject with their grades
    enrolled_students = db.query("""
        SELECT s.student_id, s.name as student_name, ps.calification
        FROM students s
        LEFT JOIN person_subject ps ON s.student_id = ps.person_id AND ps.subject_id = %s
        ORDER BY s.name
    """, (subject_id,))
    
    return render_template('asignatura.html', subject=subject, students=enrolled_students)

@app.route('/update_grade/<int:student_id>', methods=['POST'])
def update_grade(student_id):
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        calification = request.form.get('calification')
        
        # Check if the grade already exists for this student and subject
        existing_grade = db.query_one(
            "SELECT * FROM person_subject WHERE person_id = %s AND subject_id = %s",
            (student_id, subject_id)
        )
        
        if existing_grade:
            # Update existing grade
            db.execute(
                "UPDATE person_subject SET calification = %s WHERE person_id = %s AND subject_id = %s",
                (calification, student_id, subject_id)
            )
        else:
            # Insert new grade
            db.execute(
                "INSERT INTO person_subject (person_id, subject_id, calification) VALUES (%s, %s, %s)",
                (student_id, subject_id, calification)
            )
        
        return redirect(url_for('asignatura', subject_id=subject_id))

@app.route('/alumnos')
def alumnos():
    # Fetch all students from the database
    students = db.query("SELECT * FROM students ORDER BY name")
    return render_template('alumnos.html', students=students)

@app.route('/nuevo_alumno')
def nuevo_alumno():
    return render_template('nuevo_alumno.html')

@app.route('/crear_alumno', methods=['POST'])
def crear_alumno():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        dni = request.form.get('dni')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        
        # Validate required fields
        if not name or not dni or not email:
            return render_template('nuevo_alumno.html', error="Todos los campos marcados con * son obligatorios")
        
        try:
            # Insert new student
            db.execute(
                "INSERT INTO students (name, dni, phone, email, address) VALUES (%s, %s, %s, %s, %s)",
                (name, dni, phone, email, address)
            )
            
            # Redirect to students list
            return redirect(url_for('alumnos'))
        except Exception as e:
            # Handle errors (e.g., duplicate DNI or email)
            error_msg = str(e)
            if "Duplicate entry" in error_msg:
                if "dni" in error_msg:
                    error_msg = "Error: El DNI/NIE ya existe en el sistema"
                elif "email" in error_msg:
                    error_msg = "Error: El email ya existe en el sistema"
                    
            return render_template('nuevo_alumno.html', error=error_msg)

@app.route('/alumno/<int:student_id>/notas')
def student_grades(student_id):
    # Get student information
    student = db.query_one("SELECT * FROM students WHERE student_id = %s", (student_id,))
    if not student:
        return "Alumno no encontrado", 404
    
    # Get all subjects and the student's grades
    subjects_with_grades = db.query("""
        SELECT s.subject_id, s.name, s.hours_per_week, ps.calification
        FROM subject s
        LEFT JOIN person_subject ps ON s.subject_id = ps.subject_id AND ps.person_id = %s
        ORDER BY s.name
    """, (student_id,))
    
    return render_template('student_grades.html', student=student, subjects=subjects_with_grades)

if __name__ == '__main__':
    app.run(debug=True, port=80)