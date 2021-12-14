from flask import render_template, url_for, flash, request, redirect
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc, or_
from is_safe_url import is_safe_url
from . import app, db
from .models import *
from .forms import *
import functions

@app.route("/admin/skill")
def admin_skill_list():
    return render_template("admin/skill/list.html")