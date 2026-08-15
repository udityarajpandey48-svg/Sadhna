import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for , session
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash , check_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY" , "dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# bed_time = request.form.get('tobed')
# wakeup_time = request.form.get('wakeup')
# japacomplete_time = request.form.get('japa')

# ammountof_daysleep_in_minuts = int(request.form.get("daysleep", 0) or 0)

# present_or_not_mangal_points = request.form.get("mangalarati")
# present_or_not_class_points = request.form.get("morningclass")
# present_or_not_book_points = request.form.get("spbook")
# present_or_not_clean_points = request.form.get("clean")


def calculate_bed_points(bed_time):
    time_value = datetime.strptime(bed_time, "%H:%M").time()

    if time_value <= datetime.strptime("21:30", "%H:%M").time():
        return 20
    elif time_value <= datetime.strptime("21:45", "%H:%M").time():
        return 15
    elif time_value <= datetime.strptime("22:00", "%H:%M").time():
        return 10
    elif time_value <= datetime.strptime("22:15", "%H:%M").time():
        return 5
    else:
        return 0

def calculate_wakeup_points(wakeup_time):
    time_value = datetime.strptime(wakeup_time, "%H:%M").time()

    if time_value <= datetime.strptime("03:30", "%H:%M").time():
        return 20
    elif time_value <= datetime.strptime("03:45", "%H:%M").time():
        return 15
    elif time_value <= datetime.strptime("04:00", "%H:%M").time():
        return 10
    elif time_value <= datetime.strptime("04:15", "%H:%M").time():
        return 5
    else:
        return 0

def calculate_japacomplete_points(japacomplete_time):
    time_value = datetime.strptime(japacomplete_time, "%H:%M").time()

    if time_value <= datetime.strptime("07:30", "%H:%M").time():
        return 20
    elif time_value <= datetime.strptime("09:00", "%H:%M").time():
        return 15
    elif time_value <= datetime.strptime("13:00", "%H:%M").time():
        return 10
    elif time_value <= datetime.strptime("15:00", "%H:%M").time():
        return 5
    else:
        return 0

def calculate_daysleep_points(ammountof_daysleep_in_minuts):
    time_value = ammountof_daysleep_in_minuts
    if time_value <= 30:
        return 20
    elif time_value <= 60 and time_value >30:
        return 10
    elif time_value > 60:
        return 5
    else:
        return 0

# def calculate_mangalarati_points(value):
#     if value == "yes":
#         return 20
#     else:
#         return 0


# def calculate_bookreading_points(present_or_not_book_points):
#     if present_or_not_book_points == "completed":
#         return 10
#     else:
#         return 0

# def calculate_class_points(present_or_not_class_points):
#     if present_or_not_class_points == "attended":
#         return 20
#     else:
#         return 0

# def calculate_clean_points(present_or_not_clean_points):
#     if present_or_not_clean_points == "completed":
#         return 5
#     else:
#         return 0


    

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    studentid = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(200), nullable=False)




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
    total = db.Column(db.Integer)

with app.app_context():
    db.create_all()

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

@app.route("/addsadhana", methods=["GET", "POST"])
def addsadhana():

    studentid = session.get("studentid")

    if not studentid:
        return redirect(url_for("login"))

    if request.method == "POST":

        bed_points = calculate_bed_points(
            request.form.get("tobed")
        )

        wake_points = calculate_wakeup_points(
            request.form.get("wakeup")
        )

        japa_points = calculate_japacomplete_points(
            request.form.get("japa")
        )

        day_sleep_points = calculate_daysleep_points(
            int(request.form.get("daysleep", 0) or 0)
        )

        mangal_points = int(request.form.get("mangalarati"))
    

        class_points = int(request.form.get("morningclass"))

        book_points = int(request.form.get("spbook"))

        clean_points = int(request.form.get("clean"))


        sadhana = Sadhana(
            studentid=studentid,
            bed_points=bed_points,
            wake_points=wake_points,
            day_sleep_points=day_sleep_points,
            japa_points=japa_points,
            mangal_points=mangal_points,
            class_points=class_points,
            book_points=book_points,
            clean_points=clean_points,
        )

        db.session.add(sadhana)
        db.session.commit()

        return redirect(url_for("addsadhana"))

    sadhana = Sadhana.query.filter_by(
        studentid=studentid
    ).order_by(
        Sadhana.id.desc()
    ).first()

    return render_template(
        "addsadhana.html",
        sadhana=sadhana
    )


if __name__ == "__main__":
    app.run()