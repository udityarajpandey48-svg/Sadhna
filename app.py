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

class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.String(20), db.ForeignKey("student.studentid"))
    score = db.Column(db.Integer)

class Sadhana(db.Model):
    __tablename__ = "sadhana"
    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.String(20), db.ForeignKey("student.studentid"))
    bed_points = db.Column(db.Integer , default=0)
    wake_points = db.Column(db.Integer , default=0)
    day_sleep_points = db.Column(db.Integer , default=0)
    japa_points = db.Column(db.Integer , default=0)
    mangal_points = db.Column(db.Integer , default=0)
    class_points = db.Column(db.Integer , default=0)
    book_points = db.Column(db.Integer , default=0)
    clean_points = db.Column(db.Integer , default=0)
    total = db.column(db.Integer)

@app.route("/")
def home():
    leaderboard = db.session.query(Student , Score).join(Score , Student.studentid == Score.studentid).order_by(Score.score.desc()).all()

    return render_template("index.html", leaderboard=leaderboard)
 


@app.route("/login" , methods=["GET" , "POST"])
def login():
    if request.method == "POST":

        studentid = request.form.get("studentid")
        password = request.form.get("password")

        student = Student.query.filter_by(studentid=studentid).first()

        if student and check_password_hash(student.password, password):
            session["studentid"] = student.studentid
            return redirect(url_for("userprofile"))
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

    return render_template("register.html")

@app.route("/userprofile")
def userprofile():
    return render_template("userprofile.html")

@app.route("/addsadhana" , methods=('GET' , 'POST'))
def addsadhana():
    if request.method == 'POST':
        bed_points = request.form.get("tobed")
        wake_points = request.form.get("wakeup")
        day_sleep_points = request.form.get("daysleep")
        japa_points = request.form.get("japa")
        mangal_points = request.form.get("mangalarati")
        class_points = request.form.get("morningclass")
        book_points = request.form.get("spbook")
        clean_points = request.form.get("clean")


        sadhana = Sadhana(
        bed_points  = bed_points,
        wake_points  = wake_points,
        day_sleep_points  = day_sleep_points ,
        japa_points  = japa_points ,
        mangal_points = mangal_points ,
        class_points  = class_points,
        book_points  = book_points,
        clean_points  = clean_points)

        db.session.add(sadhana)
        db.session.commit()

        return redirect("addsadhana.html")

        
        
    studentid = db.session.get("studentid")
    sadhana = Sadhana.query.filter_by(studentid=studentid).order_by(studentid).first()
    return render_template("addsadhana.html")

# @app.route("/logout")
# def logout():

#     session.pop("studentid", None)

#     return redirect(
#         url_for("login")
#     )

if __name__ == "__main__":
    app.run()