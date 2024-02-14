from flask_wtf import FlaskForm

class EditProfileForm(FlaskForm):
    pass
    # username = StringField("Username", validators=[DataRequired(), Length(min=4, max=12)], render_kw={"placeholder": "Enter your username"})
    # fullname = StringField("Full Name", validators=[Length(min=4, max=16)], render_kw={"placeholder": "Enter your full name"})
    # bio = TextAreaField("Bio", render_kw={"placeholder": "Enter your bio"})
    # profile_pic = FileField("Profile Picture", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    # submit = SubmitField("Update Profile")