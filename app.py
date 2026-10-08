from flask import Flask, request, render_template, redirect, url_for
import boto3
import pymysql

app = Flask(__name__)
import os
import boto3
import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
BUCKET_NAME = os.environ.get('S3_BUCKET')

db = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
bucket_name="student-photo-demo-gopu"

db=pymysql.connect(
    host="database-1.cn4ycqy029xm.eu-north-1.rds.amazonaws.com",
    port=3306,
    user="admin",
    password="Joeronaldo&7",
    database="studentdb"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    course = request.form.get('course', '')
    photo = request.files.get('photo')

    if not photo:
        return "No photo uploaded", 400

    bucket_name = 'joe-student-photos-2026'
    s3 = boto3.client('s3', region_name='eu-north-1')

    # Upload to S3 without ACLs
    s3.upload_fileobj(
        photo,
        bucket_name,
        photo.filename
    )

    photo_url = f"https://{bucket_name}.s3.eu-north-1.amazonaws.com/{photo.filename}"

    # Insert into RDS
    cursor = db.cursor()
    sql = "INSERT INTO students (name, email, course, photo_url) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, email, course, photo_url))
    db.commit()
    cursor.close()

    return "Student Registered Successfully"
    return redirect(url_for('list_students'))
@app.route('/students', methods=['GET'])
def list_students():
    cursor = db.cursor()
    cursor.execute("SELECT name, email, course, photo_url FROM students")
    students = cursor.fetchall()
    cursor.close()
    return render_template('students.html', students=students)
if __name__=="__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
