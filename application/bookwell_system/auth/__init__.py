from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
from ..models import *
