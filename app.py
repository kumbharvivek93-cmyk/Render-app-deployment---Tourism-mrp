from flask import Flask,redirect,render_template,url_for,session,flash,request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta,datetime

app=Flask(__name__)
app.secret_key="vivekkali"
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///Tourist.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.permanent_session_lifetime=timedelta(minutes=60)
db=SQLAlchemy(app)

def validator_string(string_v):
    if not string_v or string_v.strip()==""or len(string_v)<2:
        return f"enter a valid {string_v}"

class Tourist(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    mobile_no=db.Column(db.String(13),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(30))

class criminals(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    rname=db.Column(db.String(30),nullable=False)
    rmobile_no=db.Column(db.String(13),nullable=False)
    raddress=db.Column(db.String(100),nullable=False)
    discription=db.Column(db.String(500),nullable=False)


with app.app_context():
    db.create_all()
    print("Database is created !")



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    session.permanent=True
    if request.method=="POST":
        name=request.form.get("name")
        mobile_no=request.form.get("mobile_no")
        email=request.form.get("email")
        password=request.form.get("password")

        validator_string(name)
        validator_string(password)
        validator_string(email)

        if len(mobile_no)!=10:
            return "enter a valid mobile no !"
        
        session['name']=name

        new_user=Tourist(
            name=name,
            mobile_no=mobile_no,
            email=email,
            password=password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            print("user added in the database !")
            return redirect(url_for("complaint"))
        except Exception as e :
            db.session.rollback()
            print(e)
            return render_template("singup.html")


    else:
        return render_template("signup.html")
    
@app.route("/login",methods=["GET","POST"])
def login():
    session.permanent=True
    if request.method=="POST":
        mobile_no=request.form.get("mobile_no")
        password=request.form.get("password")

        validator_string(mobile_no)
        validator_string(password)

        user=Tourist.query.filter_by(mobile_no=mobile_no).first()

        if user and user.password==password:
            flash(f"logged in successfully ")
            return redirect(url_for("complaint"))
        else:
            flash("user not found")
            return render_template("login.html")
    else:
        return render_template("login.html")
        
@app.route("/complaint",methods=['GET','POST'])
def complaint():
    session.permanent=True
    if request.method=="POST":
        rname=request.form.get("rname")
        rmobile_no=request.form.get("rmobile_no")
        raddress=request.form.get("raddress")
        discription=request.form.get("discription")
        

        validator_string(rname)
        validator_string(rmobile_no)
        validator_string(raddress)
        validator_string(discription)

        session['rname']=rname

        new_criminal=criminals(
            rname=rname,
            rmobile_no=rmobile_no,
            raddress=raddress,
            discription=discription
        )

        try:
            db.session.add(new_criminal)
            db.session.commit()
            return f"thank you for complainting against {session['rname']} your complaint is srored we well look up soon and notify you the reaponse thank you ! "
        except Exception as e :
            db.session.rollback()
            print(e)
            flash("something went wrong !")
            return render_template("complaint.html")
    else:
        return render_template("complaint.html")
    
if __name__=="__main__":
    app.run()


