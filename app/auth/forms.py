from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models.user import User
from wtforms import ValidationError


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Mobile Number")
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField( "Confirm Password", validators=[DataRequired()] )
    submit = SubmitField( "Register" )

    def validate_email(self, field):
        user = User.get_by_email(field.data)
        if not user:
            raise ValidationError("Email already exists!")

    def validate_username(self, field):
        user = User.get_by_username(field.data)
        if not user:
            raise ValidationError("Username already exists!")


class ForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


class ResetPasswordForm(FlaskForm):
    password = PasswordField( "Password", validators=[DataRequired(), EqualTo( 'confirm' )] )
    confirm = PasswordField( "Confirm Password", validators=[DataRequired()] )
    submit = SubmitField("Submit")