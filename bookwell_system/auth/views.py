from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from is_safe_url import is_safe_url

from . import auth
from .. import db
from ..models import User
from .forms import RegistrationForm, LoginForm
from ..functions import flash_errors

@auth.route("/register", methods=['GET','POST'])
def register():
    next=request.args.get('next')
    if current_user.is_authenticated:
        flash("You've already logged in!")
        return redirect(next or url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,password=form.password.data,first_name=form.first_name.data,last_name=form.last_name.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Congratulations! Your registration has completed.")
        if not is_safe_url(next, request.url_root):
            return redirect(url_for('main.home'))
        return redirect(next or url_for('main.home'))
    else:
        flash_errors(form)
    return render_template('auth/register.html', title='Register', form=form)


@auth.route("/login", methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data): 
            login_user(user)
            flash("Login Success!")
            next=request.args.get('next')
            if not is_safe_url(next, request.url_root):
                return redirect(url_for('main.home'))
            return redirect(next or url_for('main.home'))
        else:
            flash("Email or Password incorrect.")
    else:
        flash_errors(form)
    return render_template('auth/login.html', title='Login', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    flash("You have successfully logged out!")
    next=request.args.get('next')
    if not is_safe_url(next, request.url_root):
        return redirect(url_for('main.home'))
    return redirect(next or url_for('main.home'))