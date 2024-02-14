from flask import Blueprint, render_template
from flask_login import login_required

from website.models import User, Member

views = Blueprint("views", __name__)

@views.route("/")
def index():
    members = Member.query.order_by(Member.rating.desc()).limit(5)
    return render_template("index.html", members=members)

@views.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html", title="Leaderboard")

@views.route("/tournaments")
def tournaments():
    return render_template("tournaments.html", title="Tournaments")

@views.route("/<string:user_id>")
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    return render_template("profile.html", title=f"Profile - {user.fullname}", user=user)