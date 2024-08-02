from flask_login import UserMixin
from sqlalchemy.sql import func, case
from sqlalchemy.ext.hybrid import hybrid_property

from website import db

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(63), nullable=False)
    username = db.Column(db.String(15), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    register_date = db.Column(db.DateTime, default=func.now())

class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(63), nullable=False)
    class_name = db.Column(db.String(15), nullable=False)  # change to year
    is_active = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Integer, default=800)
    register_date = db.Column(db.DateTime, default=func.now())

    white_matches = db.relationship("Match", foreign_keys="Match.white_player_id", backref="white_player", lazy=True)
    black_matches = db.relationship("Match", foreign_keys="Match.black_player_id", backref="black_player", lazy=True)
    tournaments = db.relationship("Tournament", secondary="participants", back_populates="participants", lazy=True)

    @hybrid_property
    def total_matches(self):
        return self.matches_won + self.matches_lost + self.matches_drawn

    @total_matches.expression
    def total_matches(cls):
        return cls.matches_won + cls.matches_lost + cls.matches_drawn

    @hybrid_property
    def matches_won(self):
        return len([match for match in self.white_matches if match.winner == "White"]) + \
               len([match for match in self.black_matches if match.winner == "Black"])

    @matches_won.expression
    def matches_won(cls):
        return (
            func.sum(case((Match.winner == "White", 1), else_=0)).filter(Match.white_player_id == cls.id) +
            func.sum(case((Match.winner == "Black", 1), else_=0)).filter(Match.black_player_id == cls.id)
        )

    @hybrid_property
    def matches_lost(self):
        return len([match for match in self.white_matches if match.winner == "Black"]) + \
               len([match for match in self.black_matches if match.winner == "White"])

    @matches_lost.expression
    def matches_lost(cls):
        return (
            func.sum(case((Match.winner == "Black", 1), else_=0)).filter(Match.white_player_id == cls.id) +
            func.sum(case((Match.winner == "White", 1), else_=0)).filter(Match.black_player_id == cls.id)
        )

    @hybrid_property
    def matches_drawn(self):
        return len([match for match in self.white_matches if match.winner == "Draw"]) + \
               len([match for match in self.black_matches if match.winner == "Draw"])

    @matches_drawn.expression
    def matches_drawn(cls):
        return (
            func.sum(case((Match.winner == "Draw", 1), else_=0)).filter(Match.white_player_id == cls.id) +
            func.sum(case((Match.winner == "Draw", 1), else_=0)).filter(Match.black_player_id == cls.id)
        )

    @hybrid_property
    def win_rate(self):
        return self.matches_won / self.total_matches if self.total_matches > 0 else 0.0

    @win_rate.expression
    def win_rate(cls):
        return case(
            (cls.total_matches > 0, cls.matches_won / cls.total_matches),
            else_=0.0
        )

    @hybrid_property
    def draw_rate(self):
        return self.matches_drawn / self.total_matches if self.total_matches > 0 else 0.0

    @draw_rate.expression
    def draw_rate(cls):
        return case(
            (cls.total_matches > 0, cls.matches_drawn / cls.total_matches),
            else_=0.0
        )

    @hybrid_property
    def loss_rate(self):
        return self.matches_lost / self.total_matches if self.total_matches > 0 else 0.0

    @loss_rate.expression
    def loss_rate(cls):
        return case(
            (cls.total_matches > 0, cls.matches_lost / cls.total_matches),
            else_=0.0
        )
    
class Tournament(db.Model):
    __tablename__ = "tournaments"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(31), nullable=False)
    time_control_duration = db.Column(db.Integer, nullable=False)
    time_control_increment = db.Column(db.Integer, nullable=False)
    pairing_system = db.Column(db.String(15), nullable=False) # "Swiss System", "Round-Robin", "Elimination", "Custom"
    number_of_rounds = db.Column(db.Integer, nullable=False)
    current_round = db.Column(db.Integer, default=1)
    tournament_date = db.Column(db.DateTime, default=func.now())
    tournament_end_date = db.Column(db.DateTime)
    
    matches = db.relationship("Match", foreign_keys="Match.tournament_id", backref="tournament", lazy=True)
    participants = db.relationship("Member", secondary="participants", back_populates="tournaments", lazy=True)

class Match(db.Model):
    __tablename__ = "matches"
    id = db.Column(db.Integer, primary_key=True)
    time_control_duration = db.Column(db.Integer, nullable=False)
    time_control_increment = db.Column(db.Integer, nullable=False)
    tournament_round = db.Column(db.Integer)
    winner = db.Column(db.String(5))  # "White", "Black", "Draw", Null (not determined)
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

    @hybrid_property
    def score(self):
        # Implement your logic to calculate score
        return 0  # Replace with actual calculation

    @score.expression
    def score(cls):
        # Implement SQL expression for score calculation
        return 0  # Replace with actual SQL expression

    @hybrid_property
    def bhc1_score(self):
        # Implement your logic to calculate BHC1
        return 0  # Replace with actual calculation

    @bhc1_score.expression
    def bhc1_score(cls):
        # Implement SQL expression for BHC1 calculation
        return 0  # Replace with actual SQL expression

    @hybrid_property
    def bh_score(self):
        # Implement your logic to calculate BH
        return 0  # Replace with actual calculation

    @bh_score.expression
    def bh_score(cls):
        # Implement SQL expression for BH calculation
        return 0  # Replace with actual SQL expression

    @hybrid_property
    def bhc1_rating(self):
        # Implement your logic to calculate BHC1 rating
        return 0  # Replace with actual calculation

    @bhc1_rating.expression
    def bhc1_rating(cls):
        # Implement SQL expression for BHC1 rating calculation
        return 0  # Replace with actual SQL expression

    @hybrid_property
    def bh_rating(self):
        # Implement your logic to calculate BH rating
        return 0  # Replace with actual calculation

    @bh_rating.expression
    def bh_rating(cls):
        # Implement SQL expression for BH rating calculation
        return 0  # Replace with actual SQL expression