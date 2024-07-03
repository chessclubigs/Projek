from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import login_required
from sqlalchemy import func, case

from website import db
from website.models import User, Member, Match, Tournament, Participant
from website.forms.tournaments import CreateTournamentForm
from website import utils

views = Blueprint("views", __name__)

@views.route("/set_timezone_offset", methods=["POST"])
def set_timezone_offset():
    data = request.get_json()
    session["timezoneOffset"] = data.get("timezoneOffset")

    return jsonify({"message": "Timezone offset received"}), 200

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
    members = Member.query.order_by(Member.rating.desc(), Member.full_name).paginate(page=page, per_page=15)

    return render_template("leaderboard-top-rated.html", title="Leaderboard", members=members, page=page)

@views.route("/leaderboard/win-rate")
def leaderboard_win_rate():
    page = request.args.get("page", 1, type=int)
    members = Member.query\
        .outerjoin(Match, ((Match.white_player_id == Member.id) | (Match.black_player_id == Member.id)))\
        .group_by(Member.id)\
        .order_by(Member.win_rate.desc(), Member.draw_rate.desc(), Member.full_name)\
        .paginate(page=page, per_page=15)

    return render_template("leaderboard-win-rate.html", title="Leaderboard", members=members, page=page)

@views.route("/leaderboard/tournaments-participated")
def leaderboard_tournaments_participated():
    page = request.args.get("page", 1, type=int)
    members = Member.query.outerjoin(Member.tournaments).group_by(Member.id).order_by(func.count(Tournament.id).desc()).paginate(page=page, per_page=15)

    return render_template("leaderboard-tournaments-participated.html", title="Leaderboard", members=members, page=page)

@views.route("/tournaments")
def tournaments():
    tournaments = Tournament.query.order_by(Tournament.tournament_date.desc()).all()
    timezone_offset = session.get("timezoneOffset")

    return render_template("tournaments.html", title="Tournaments", tournaments=tournaments, timezone_offset=timezone_offset, utils=utils)

@views.route("/tournaments/create", methods=["GET", "POST"])
def tournaments_create():
    form = CreateTournamentForm()

    if form.validate_on_submit():
        new_tournament = Tournament(
            title=form.title.data,
            time_control_duration=60 * form.time_control_minutes.data + form.time_control_seconds.data,
            time_control_increment=form.time_control_increment.data,
            matching_system=form.matching_system.data,
            number_of_rounds=form.number_of_rounds.data
        )

        db.session.add(new_tournament)
        db.session.commit()

        for member in form.participants.data:
            member_id = member.id
            participant = Participant(tournament_id=new_tournament.id, member_id=member_id)
            db.session.add(participant)
        
        db.session.commit()

        flash("Tournament created successfully!", "success")
        return redirect(url_for("views.tournaments"))

    return render_template("tournaments-create.html", title="Create Tournament", form=form)

@views.route("/<string:user_id>")
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    return render_template("profile.html", title=f"Profile | {user.fullname}", user=user)