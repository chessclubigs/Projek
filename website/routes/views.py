from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required

from website.models import User, Member

views = Blueprint("views", __name__)

@views.app_context_processor
def inject_members():
    aside_ctx = {
        "members": Member.query.order_by(Member.rating.desc()).limit(5)
    }
    return {"aside_ctx": aside_ctx}

@views.route("/")
def index():
    return render_template("index.html")

@views.route("/leaderboard")
def leaderboard():
    return redirect(url_for("views.leaderboard_top_rated"))

@views.route("/leaderboard/top-rated")
def leaderboard_top_rated():
    page = request.args.get("page", 1, type=int)
    members = Member.query.order_by(Member.rating.desc())\
        .paginate(page=page, per_page=10)
    return render_template("leaderboard-top-rated.html", title="Leaderboard", members=members)

@views.route("/leaderboard/win-rate")
def leaderboard_win_rate():
    page = request.args.get("page", 1, type=int)
    members = Member.query.order_by(Member.rating.desc())\
        .paginate(page=page, per_page=10)
    return render_template("leaderboard-win-rate.html", title="Leaderboard", members=members)

@views.route("/leaderboard/tournaments-participated")
def leaderboard_tournaments_participated():
    page = request.args.get("page", 1, type=int)
    members = Member.query.order_by(Member.rating.desc())\
        .paginate(page=page, per_page=10)
    return render_template("leaderboard-tournaments-participated.html", title="Leaderboard", members=members)

@views.route("/tournaments")
def tournaments():
    return render_template("tournaments.html", title="Tournaments")

@views.route("/<string:user_id>")
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    return render_template("profile.html", title=f"Profile | {user.fullname}", user=user)