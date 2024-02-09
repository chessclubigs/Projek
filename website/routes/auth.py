from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import logout_user

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("login.html", title="Login")

@auth.route("/logout")
def logout():
    logout_user()
    flash("Successfully logged out.", "success")
    return redirect(url_for("auth.login"))