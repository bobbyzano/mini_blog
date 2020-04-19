from flask import Flask, request,render_template, redirect, flash, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from flask_admin import Admin
from flask_mail import Mail



#instantiate flask class
app = Flask(__name__)

app.config.from_object(Config)

#creating db object
db = SQLAlchemy(app)
#createing moment object
moment = Moment(app)
#creating login object
login = LoginManager(app)
login.session_protection = 'strong'
login.login_view = 'login'

admin = Admin(app)
mail = Mail(app)
#seperation of concerns
from app import routes, models, forms


