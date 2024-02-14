from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user

from website.forms.auth import LoginForm
from website.models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.index"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for("views.index"))
        return redirect(url_for("auth.login"))

    return render_template("login.html", title="Login", form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))