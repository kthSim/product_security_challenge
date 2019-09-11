from project import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from project.forms import LoginForm, RegisterNewUserForm
from project.models import User


@app.route("/")
def welcome():
    return render_template("base.html", title='Zendesk Security Challenge')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))

    form = LoginForm()

    if form.validate_on_submit():
        #user = User.query.filter_by(username=form.username.data).first()
        user = User.query.filter(User.username == form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Apologies but that is an Invalid username/password combination")
            return redirect(url_for('login'))
        else:
            flash('Login Requested for user {}, remember_me={}'.format(form.username.data, form.rmbr_user.data))
            login_user(user, remember=form.rmbr_user.data)
            ret_page = request.args.get('next')

            if not ret_page:
                ret_page = url_for('welcome')

            return redirect(ret_page)

    return render_template("login.html", title="Log In", form=form)


@app.route("/logout")
def logout():
    flash("{}, you have been logged out!".format(current_user.username))
    logout_user()
    return redirect(url_for('welcome'))


@app.route("/needLogin")
@login_required
def needLogin():
    return render_template("needLogin.html", title="FOOOOOOOL")


@app.route("/register")
def reg_user():
    form = RegisterNewUserForm()

    return render_template("regUser.html", title="Register", form=form)
