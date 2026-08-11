import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash , check_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY" , "dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    studentid = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login" , methods=["GET" , "POST"])
def login():
    if request.method == "POST":

        studentid = request.form.get("studentid")
        password = request.form.get("password")

        student = Student.query.filter_by(studentid=studentid).first()

        if student and check_password_hash(student.password, password):

            return f"welcome {student.fullname}"
        return "invalid student id or password"

    return render_template("login.html")


@app.route("/register" , methods=["GET" , "POST"])
def register():
    if request.method == "POST":

        fullname = request.form.get("fullname")
        studentid = request.form.get("studentid")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        if password != confirm_password:
            return "password and confirm password should be same"

        existing_student = Student.query.filter_by(studentid=studentid).first()

        if existing_student:
            return "Student ID already exists"

        existing_email = Student.query.filter_by(email=email).first()

        if existing_email:
            return "Email already exists"

        hashed_password = generate_password_hash(password)

        student = Student(
            fullname = fullname,
            studentid = studentid,
            email = email,
            phone = phone,
            password = hashed_password )

        db.session.add(student)
        db.session.commit()
        
    return redirect(url_for("login"))





if __name__ == "__main__":
    app.run()