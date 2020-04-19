from flask import request,render_template, redirect, flash, url_for
from app import app
from app.forms import LoginForm, RegisterForm, ContactForm
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, blogTable
from datetime import datetime
from app import db, mail
from flask_mail import Message

#index endpoint
@app.route("/")
def index():
    page = request.args.get('page', 1 , type=int)
    posts = blogTable.query.order_by(blogTable.date.desc()).paginate(page, app.config['POST_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None

    return render_template("index.html",posts=posts.items,  next_url=next_url, prev_url=prev_url)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/addblog")
def add():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']

    post = blogTable(title=title, author=author, content=content, date=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route("/post/<int:post_id>")
def post(post_id):
    post = blogTable.query.get_or_404(post_id)
    return render_template("post.html", post=post)

 
@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        msg = Message(subject=form.subject.data, sender=form.email.data, recipients=['recipient@gmail.com'])
        msg.body = """
        FROM: %s,
        EMAIL: <%s>,
        # WEBSITE: %s
        MESSAGE: %s
        """ % (form.name.data, form.email.data, form.website.data, form.message.data)
        mail.send(msg)
        flash("message has been sent", "success")
        return redirect(request.url)
    return render_template("contact.html", form=form)
#the login endpoint
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash("Successfully logged in", "success")
                # return to attemted protected routes after successfully logged in
                return redirect(url_for('index'))
            flash("Invalid email or password", "info")
            return render_template("login.html", form=form)
        flash("Invalid email or password", "danger")
        return render_template("login.html", form=form)
    return render_template("login.html", form=form)    

#the register endpoint
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST":
        #create an object and pass the hashed password
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        data = User.query.filter_by(email=form.email.data).first()
        if data:
            #check if email alredy in the database
            if data.email == form.email.data:
                flash("User already exist", "danger")
                return render_template("register.html", form=form)
        user = User(email=form.email.data,username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Successfully registered ", "success")
        return redirect(url_for("login"))
        
    return render_template("register.html", form=form)

#logging out endpoint
@app.route('/logout')
#@login_required
def logout():
    logout_user()
    flash('You are now logged out', "success")
    return redirect(url_for('login'))
