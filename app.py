from flask import Flask, redirect, render_template, url_for, session, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "vivekkali"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "Tourist.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=60)

db = SQLAlchemy(app)

def validator_string(value, field_name):
    if not value or value.strip() == "" or len(value) < 2:
        return f"Enter a valid {field_name}"
    return None


class Tourist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    mobile_no = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Criminal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rname = db.Column(db.String(30), nullable=False)
    rmobile_no = db.Column(db.String(13), nullable=False)
    raddress = db.Column(db.String(100), nullable=False)
    discription = db.Column(db.String(500), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    session.permanent = True

    if request.method == "POST":
        name = request.form.get("name")
        mobile_no = request.form.get("mobile_no")
        email = request.form.get("email")
        password = request.form.get("password")

        for value, field in [(name, "name"), (email, "email"), (password, "password")]:
            error = validator_string(value, field)
            if error:
                return error

        if not mobile_no or len(mobile_no) != 10:
            return "Enter a valid mobile number!"

  
        hashed_password = generate_password_hash(password)

        new_user = Tourist(
            name=name,
            mobile_no=mobile_no,
            email=email,
            password=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            session['name'] = name
            flash("Signup successful!")
            return redirect(url_for("complaint"))
        except Exception as e:
            db.session.rollback()
            print(e)
            flash("Error during signup")
            return render_template("signup.html")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.permanent = True

    if request.method == "POST":
        mobile_no = request.form.get("mobile_no")
        password = request.form.get("password")

        error = validator_string(mobile_no, "mobile number")
        if error:
            return error

        user = Tourist.query.filter_by(mobile_no=mobile_no).first()

        if user and check_password_hash(user.password, password):
            session['name'] = user.name
            flash("Logged in successfully!")
            return redirect(url_for("complaint"))
        else:
            flash("Invalid credentials")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    session.permanent = True

    if request.method == "POST":
        rname = request.form.get("rname")
        rmobile_no = request.form.get("rmobile_no")
        raddress = request.form.get("raddress")
        discription = request.form.get("discription")

        for value, field in [
            (rname, "name"),
            (rmobile_no, "mobile number"),
            (raddress, "address"),
            (discription, "description")
        ]:
            error = validator_string(value, field)
            if error:
                return error

        new_criminal = Criminal(
            rname=rname,
            rmobile_no=rmobile_no,
            raddress=raddress,
            discription=discription
        )

        try:
            db.session.add(new_criminal)
            db.session.commit()
            return f"Complaint against {rname} stored successfully!"
        except Exception as e:
            db.session.rollback()
            print(e)
            flash("Something went wrong!")
            return render_template("complaint.html")

    return render_template("complaint.html")

