from ..functions import get_week
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from is_safe_url import is_safe_url
from datetime import datetime

from . import main
from .. import db
from ..models import User
from ..functions import get_week
# from .forms import RegistrationForm, LoginForm

@main.route("/", methods=['GET','POST'])
def home():
    return str(get_week(datetime.now()))