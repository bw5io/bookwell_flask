from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views
from ..models import *
