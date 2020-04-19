from flask_login import  UserMixin, current_user
from app import db
from app import login, admin
from app import app
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
# import flask_whooshalchemy as wa


#user model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column (db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        
        

    # helper function to login users
    @login.user_loader
    def load_user(id):
        return User.query.get(id)



class blogTable(db.Model):
    __tablename__ = 'blogtable'
    id = db.Column (db.Integer, primary_key=True)
    title = db.Column (db.String(45), unique=True, nullable=False)
    author = db.Column(db.String(20))
    date = db.Column(db.DateTime, default=datetime.utcnow )
    content = db.Column (db.String(5000), unique=True, nullable=False)

    def __init__(self, title, author, date, content):
        self.title = title
        self.author = author
        self.date = date
        self.content = content



class MyModelView(ModelView):
    def is_accessible(self):
        # return current_user.is_authenticated
        user = User.query.filter_by(admin=True).one()
        if user.admin:
            return current_user.admin


    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(blogTable, db.session))


db.create_all()