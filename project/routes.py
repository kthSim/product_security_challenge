from project import app, db
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from project.forms import LoginForm, RegisterNewUserForm, PasswordResetRequestForm, PasswordResetForm
from project.models import User
from project.email import send_email_password_reset


@app.route("/")
def welcome():
    print(session)
    print()
    return render_template("home.html", title='Zendesk Security Challenge')


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('welcome'))

    form = LoginForm()

    if form.validate_on_submit():
        #user = User.query.filter_by(username=form.username.data).first()
        user = User.query.filter(User.username == form.username.data).first()

        if user is None or not user.check_password(form.password.data) or user.lockout:

            if user is not None:

                user.fail_count = user.fail_count + 1
                db.session.commit()

                if user.fail_count > 5:
                    user.lockout = True
                    db.session.commit()

                    app.logger.info("User[{}]'s account is locked")
                    flash("Your account has been locked due to excessive failed login attempts,"
                          "please reset your password to log back in")
                    return redirect(url_for('reset_password_request'))

            flash("Apologies but that is an Invalid username/password combination")
            app.logger.info("Login Attempt Failed")
            return redirect(url_for('login'))

        flash('Login Requested for user {}, remember_me={}'.format(form.username.data, form.rmbr_user.data))
        login_user(user, remember=form.rmbr_user.data)
        session['username'] = user.username

        ret_page = request.args.get('next')

        if not ret_page:
            ret_page = url_for('welcome')

        app.logger.info("Logging in user[{}]".format(form.username.data))
        return redirect(ret_page)


    return render_template("login.html", title="Log In", form=form)


@app.route("/logout")
@login_required
def logout():
    flash("{}, you have been logged out!".format(current_user.username))
    session.pop('username', None)
    session.pop('userid', None)
    app.logger.info("User[{}] has logged out".format(current_user.username))
    logout_user()
    return redirect(url_for('welcome'))


@app.route("/needLogin")
@login_required
def needLogin():
    return render_template("needLogin.html", title="FOOOOOOOL")


@app.route("/register", methods=['GET', 'POST'])
def reg_user():
    if current_user.is_authenticated:
        return redirect((url_for('index')))

    form = RegisterNewUserForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratz! You've been registered successfully, go ahead and log in~!")
        app.logger.info("New user[{}] registered".format(form.username.data))
        return redirect(url_for('login'))

    return render_template("regUser.html", title="Register", form=form)


@app.route("/reset_password_request", methods=['GET', 'POST'])
def reset_password_request():
    form = PasswordResetRequestForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()

        if user is None:
            flash("Apologies, but that email doesn't seem to be registered with us")
            return redirect(url_for('reset_password_request'))
        else:
            flash("Please check your mail for instructions to reset your password")
            send_email_password_reset(user)
            return redirect(url_for('login'))

    return render_template('resetPwdRequest.html', title="Reset your password", form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    user = User.verify_token_reset_password(token)

    if not user:
        app.logger.info("Password reset token mismatch found, redirected to welcome page")
        return redirect(url_for('welcome'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.lockout = False
        db.session.commit()
        flash('Your password has been reset!')
        app.logger.info("Password has been reset for User[{}]".format(user.username))
        return redirect(url_for('login'))

    return render_template('resetPwd.html', form=form)
