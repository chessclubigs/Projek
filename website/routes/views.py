from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route("/")
def index():
    return render_template("index.html")

@views.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html", title="Leaderboard")

@views.route("/tournaments")
def tournaments():
    return render_template("tournaments.html", title="Tournaments")