from flask_login import UserMixin
from sqlalchemy.sql import func

from website import db

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(63), nullable=False)
    username = db.Column(db.String(15), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    register_date = db.Column(db.DateTime, default=func.now())

class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(63), nullable=False)
    class_name = db.Column(db.String(15), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    rating = db.Column(db.Integer, default=800, nullable=False)
    register_date = db.Column(db.DateTime, default=func.now())

    white_matches = db.relationship("Match", foreign_keys="Match.white_player_id", backref="white_player", lazy=True)
    black_matches = db.relationship("Match", foreign_keys="Match.black_player_id", backref="black_player", lazy=True)
    tournaments = db.relationship("Tournament", secondary="participants", back_populates="participants", lazy=True)

class Tournament(db.Model):
    __tablename__ = "tournaments"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(31), nullable=False)
    game_mode = db.Column(db.String(15), nullable=False)  # "Classical", "Rapid", "Blitz", "Bullet"
    time_control = db.Column(db.String(15), nullable=False) # e.g. "5 | 2"
    number_of_rounds = db.Column(db.Integer, default=1, nullable=False)
    tournament_date = db.Column(db.DateTime, default=func.now())
    
    matches = db.relationship("Match", foreign_keys="Match.tournament_id", backref="tournament", lazy=True)
    participants = db.relationship("Member", secondary="participants", back_populates="tournaments", lazy=True)

class Match(db.Model):
    __tablename__ = "matches"
    id = db.Column(db.Integer, primary_key=True)
    game_mode = db.Column(db.String(15), nullable=False)  # "Classical", "Rapid", "Blitz", "Bullet"
    time_control = db.Column(db.String(15), nullable=False) # e.g. "5 | 2"
    tournament_round = db.Column(db.Integer)
    winner = db.Column(db.String(7))  # "White", "Black", "Draw", Null (not determined)
    white_rating_change = db.Column(db.Integer)
    black_rating_change = db.Column(db.Integer)
    match_date = db.Column(db.DateTime, default=func.now())
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"))
    white_player_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    black_player_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)

class Participant(db.Model):
    __tablename__ = "participants"
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), primary_key=True)