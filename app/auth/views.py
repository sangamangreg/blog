from flask import redirect, render_template, url_for, request, Blueprint
from app import app
from app.auth.forms import RegisterForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
from flask_login import login_required, login_user, logout_user, current_user
from app.models.user import User, ReseetPassword

users = Blueprint( "users", __name__, template_folder="templates" )


@app.route( "/register", methods=["GET", "POST"] )
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        user = User(
            register_form.name.data,
            register_form.username.data,
            register_form.email.data,
            register_form.phone.data,
            register_form.password.data,
        )
        user.save()

        # User is successfully registerd.
        # TODO: send him email via email service
        # TODO: show him flash message
        return redirect( url_for( "home" ) )

    # else:
    #     print(register_form.errors.items())

    return render_template( "auth/register.html", register_form=register_form )


@app.route( "/login", methods=["GET", "POST"] )
def login():
    next = request.args.get( 'next' )
    if not next:
        next = url_for( "home" )

    if current_user and current_user.is_authenticated:
        return redirect( next )

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.get_by_email( login_form.email.data )
        if user and user.check_password( password=login_form.password.data ):
            # successful login
            login_user( user )

            return redirect( next )
        # else:
        #     print( login_form.errors.items(), user.id, user.password_hashed  )

    return render_template( "auth/login.html", login_form=login_form )


@app.route( "/forgot-password", methods=["GET", "POST"] )
def forgot_password():
    next = request.args.get( 'next' )
    if not next:
        next = url_for( "login" )

    if current_user and current_user.is_authenticated:
        return redirect( next )

    forgot_password_form = ForgotPasswordForm()

    if forgot_password_form.validate_on_submit():
        user = User.get_by_email( forgot_password_form.email.data )
        if user:
            # user exists

            reset = ReseetPassword( user.id )
            reset.save()
            print( reset.link_hashed )
            # TODO: send email
            return redirect( next )

    return render_template( "auth/forgot-password.html", forgot_password_form=forgot_password_form )


@app.route( "/reset-password/<link>", methods=["GET", "POST"] )
def reset_password(link):
    next = request.args.get( 'next' )
    if not next:
        next = url_for( "login" )

    if current_user and current_user.is_authenticated:
        return redirect( next )

    reset_password = ReseetPassword.query.filter_by( link_hashed=link ).first()

    # if not reset_password:
    #     throw error

    user = User.get( reset_password.owner_id )
    reset_password_form = ResetPasswordForm()

    if reset_password_form.validate_on_submit():
        user.set_password( reset_password_form.password.data )
        user.save()

        return redirect( next )
    return render_template( "auth/reset-password.html", reset_password_form=reset_password_form )


@login_required
@app.route( "/logout", methods=["GET"] )
def logout():
    logout_user()
    return redirect( url_for( "home" ) )
