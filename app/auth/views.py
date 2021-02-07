from flask import redirect, render_template, url_for, request, Blueprint
from app import app
from app.auth.forms import RegisterForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
from flask_login import login_required


users = Blueprint( "users", __name__, template_folder="templates" )


@app.route( "/register", methods=["GET", "POST"] )
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        return redirect(url_for("home"))
    return render_template( "auth/register.html", register_form=register_form)


@app.route( "/login", methods=["GET", "POST"] )
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():

        next = request.get.args('next')
        if not next:
            next = url_for("home")
        return redirect(next)
    return render_template( "auth/login.html", login_form=login_form)


@app.route( "/forgot-password", methods=["GET", "POST"] )
def forgot_password():
    forgot_password_form = ForgotPasswordForm()

    if forgot_password_form.validate_on_submit():

        next = request.get.args('next')
        if not next:
            next = url_for("home")
        return redirect(next)
    return render_template( "auth/forgot-password.html", forgot_password_form=forgot_password_form)


@app.route( "/reset-password", methods=["GET", "POST"] )
def reset_password():
    reset_password_form = ResetPasswordForm()

    if reset_password_form.validate_on_submit():

        next = request.get.args('next')
        if not next:
            next = url_for("home")
        return redirect(next)
    return render_template( "auth/reset-password.html", reset_password_form=reset_password_form)


@login_required
@app.route( "/logout", methods=["GET"] )
def logout():
    redirect( url_for("home") )

