from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, SubmitField, IntegerField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import InputRequired, Length, NumberRange

from website.models import Member

class MinTwoParticipants(object):
    """
    Validates that there are at least 2 participants selected.
    """
    def __init__(self):
        self.message = "Select at least 2 participants."

    def __call__(self, form, field):
        if len(field.data) < 2:
            raise ValidationError(self.message)

class CreateTournamentForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(min=1, max=31)], render_kw={"placeholder": "Enter title name"})
    time_control_minutes = IntegerField("Time Control Minutes", validators=[NumberRange(min=0, max=300)], render_kw={"placeholder": "mins"})
    time_control_seconds = IntegerField("Time Control Seconds", validators=[NumberRange(min=0, max=59)], render_kw={"placeholder": "secs"})
    time_control_increment = IntegerField("Time Control Increment", validators=[NumberRange(min=0, max=59)], render_kw={"placeholder": "inc"})
    matching_system = SelectField("Matching System", choices=[
        ("Swiss System", "Swiss System"),
        ("Round-Robin", "Round-Robin"),
        ("Elimination", "Elimination"),
        ("Custom", "Custom")
    ], validators=[InputRequired()])
    number_of_rounds = IntegerField("Number of Rounds", validators=[InputRequired(), NumberRange(min=1)], render_kw={"placeholder": "Enter # of rounds"})
    participants = QuerySelectMultipleField("Participants", query_factory=lambda: Member.query.filter_by(is_active=True).order_by(Member.full_name).all(), allow_blank=True, get_label="full_name", validators=[MinTwoParticipants()])
    submit = SubmitField("Create Tournament")


class EditTournamentForm(FlaskForm):
    pass

class StartTournamentForm(FlaskForm):
    pass

class EndTournamentForm(FlaskForm):
    pass