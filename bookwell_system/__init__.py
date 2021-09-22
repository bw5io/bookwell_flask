from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
import os

app = Flask(__name__)   
app.config['SECRET_KEY']=os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


from . import routes
from .models import User, Post, Comment
from .views import AdminView

admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session)) 
admin.add_view(AdminView(Post, db.session)) 
admin.add_view(AdminView(Comment, db.session))
