from project import app
from flask import render_template, flash, redirect, url_for
from project.forms import LoginForm


@app.route("/")
def index():
    return render_template("base.html", title='Zendesk Security Challenge')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login Requested for user {}, remember_me={}'.format(form.username.data, form.rmbr_user.data))
        return redirect(url_for('index'))
    return render_template("login.html", title="Log In", form=form)