from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class RegistrationForm(FlaskForm):
    first_name = StringField('firstname_label', validators=[InputRequired(message='First name required'), (Length(max=25, message='First name must less than 25 characters'))])
    last_name = StringField('lastname_label', validators=[InputRequired(message='Last name required'), (Length(max=25, message='Last name must be less than 25 characters'))])
    email = StringField('email_label', validators=[InputRequired(message='Email required'), (Length(min=4, message='Email must be at least 4 characters'))])
    password = PasswordField('password_label', validators=[InputRequired(message='Password required'), (Length(min=4, message='Password must be more than 4 characters'))])
    submit_button = SubmitField('Submit')
