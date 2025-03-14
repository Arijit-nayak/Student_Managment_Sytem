from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, init_db, Student

app = Flask(__name__)
init_db(app)

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/search', methods=['GET'])
def search_student():
    query = request.args.get('query', '').strip()
    students = Student.query.filter(Student.name.ilike(f"%{query}%")).all()
    return render_template('index.html', students=students, search_query=query)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name'].strip()
    age = request.form['age'].strip()
    email = request.form['email'].strip()
    course = request.form['course'].strip()
    
    if not name or not age.isdigit() or not email or not course:
        flash('Invalid input. Please check your data.', 'danger')
        return redirect(url_for('index'))
    
    if Student.query.filter_by(email=email).first():
        flash('Email already exists!', 'danger')
        return redirect(url_for('index'))
    
    new_student = Student(name=name, age=int(age), email=email, course=course)
    db.session.add(new_student)
    db.session.commit()
    flash('Student added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name'].strip()
        age = request.form['age'].strip()
        email = request.form['email'].strip()
        course = request.form['course'].strip()
        
        if not name or not age.isdigit() or not email or not course:
            flash('Invalid input. Please check your data.', 'danger')
            return redirect(url_for('edit_student', id=id))
        
        if Student.query.filter(Student.email == email, Student.id != id).first():
            flash('Email already in use by another student!', 'danger')
            return redirect(url_for('edit_student', id=id))
        
        student.name, student.age, student.email, student.course = name, int(age), email, course
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
