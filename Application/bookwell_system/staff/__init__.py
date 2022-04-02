from flask import Blueprint

staff = Blueprint('staff', __name__)

# from . import views, errors
from . import views
from ..models import *
