from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os

app = Flask(__name__)
CSV_FILE = "students.csv"

def load_students():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE).to_dict(orient='records')
    return []

def save_students(students):
    df = pd.DataFrame(students)
    df.to_csv(CSV_FILE, index=False)

@app.route('/')
def index():
    students = load_students()
    grades = sorted(set(student['Grade'] for student in students))
    return render_template('index.html', students=students, grades=grades)

@app.route('/add', methods=['POST'])
def add_student():
    students = load_students()
    new_student = {
        'ID': request.form['id'],
        'Name': request.form['name'],
        'Subject': request.form['subject'],
        'Grade': request.form['grade'],
        'Age': request.form['age'],
        'Gender': request.form['gender']
    }
    if any(s['ID'] == new_student['ID'] for s in students):
        return "Error: Student ID already exists!", 400
    students.append(new_student)
    save_students(students)
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete_student(id):
    students = load_students()
    students = [s for s in students if s['ID'] != id]
    save_students(students)
    return redirect(url_for('index'))

@app.route('/filter', methods=['GET'])
def filter_students():
    grade = request.args.get('grade')
    students = load_students()
    filtered_students = [s for s in students if s['Grade'] == grade]
    return render_template('index.html', students=filtered_students, grades=sorted(set(s['Grade'] for s in students)))

@app.route('/export', methods=['GET'])
def export_csv():
    return send_file(CSV_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
