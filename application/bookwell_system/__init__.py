from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)   
app.config['SECRET_KEY']=os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix="/admin")

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix="/auth")

from .staff import staff as staff_blueprint
app.register_blueprint(staff_blueprint, url_prefix="/staff")

from .student import student as student_blueprint
app.register_blueprint(student_blueprint, url_prefix="/student")

from .models import *

from .views import *