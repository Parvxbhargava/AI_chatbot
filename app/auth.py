from flask import Blueprint,render_template,request,redirect,url_for,flash
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required
from app.models import User,db
from app import bcrypt

auth=Blueprint("auth",__name__)

@auth.route("/login",methods=["GET","POST"])
def login():
  if request.method=="POST":
    email=request.form.get("email")
    password=request.form.get("password")
    user=User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password,password):
      login_user(user)
      flash("Login successful","success")
      return redirect(url_for("main.chat"))
    else:
      flash("Invalid email or password","danger")

  return render_template("login.html")

@auth.route("/signup",methods=["GET","POST"])
def signup():
  if request.method=="POST":
    email=request.form.get("email")
    password=request.form.get("password")
    confirm_password=request.form.get("confirm_password")
    if password!=confirm_password:
      flash("Passwords do not match","danger")
      return redirect(url_for("auth.signup"))

    existing_user=User.query.filter_by(email=email).first()
    if existing_user:
      flash("Email already exists","warning")
    else:
      hashed_password=bcrypt.generate_password_hash(password).decode("utf-8")
      new_user=User(email=email,password=hashed_password)
      db.session.add(new_user)
      db.session.commit()
      flash("Account created successfully","success")
      return redirect(url_for("auth.login"))

  return render_template("signup.html")

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for("auth.login"))
