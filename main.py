from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vichu@2008",
    database="studentsdb"
)

cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('index.html')

# Add Student
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    reg_no = request.form['reg_no']
    branch = request.form['branch']

    sql = """
    INSERT INTO students(name, reg_no, branch)
    VALUES(%s, %s, %s)
    """

    values = (name, reg_no, branch)

    try:
        cursor.execute(sql, values)
        db.commit()
        message = "Student Added Successfully!"
    except Exception as e:
        message = f"Error: {e}"

    return render_template('index.html', message=message)

# Search Student
@app.route('/search_student', methods=['POST'])
def search_student():
    reg_no = request.form['search_reg_no']

    sql = "SELECT * FROM students WHERE reg_no = %s"
    cursor.execute(sql, (reg_no,))

    student = cursor.fetchone()

    if student:
        return render_template(
            'index.html',
            student=student
        )
    else:
        return render_template(
            'index.html',
            message="Student Not Found"
        )

if __name__ == '__main__':
    app.run(debug=True)