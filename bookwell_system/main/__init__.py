from flask import Blueprint

main = Blueprint('main', __name__)

# from . import views, errors
from . import views
from ..models import *