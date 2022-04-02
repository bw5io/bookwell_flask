from flask import render_template, redirect, request, url_for, flash
from flask_login import logout_user, current_user

from . import app

@app.errorhandler(403)
def error_403(e):
    flash("You're not authorized to visit this page. Please login.")
    if current_user.is_authenticated:
        logout_user()
        flash("You have been logged out.")
    return redirect(url_for("auth.login"))