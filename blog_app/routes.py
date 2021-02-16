from flask import render_template, url_for, flash, redirect, request
from blog_app.models import User, Post
from blog_app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from blog_app import app, db, b # b -> bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from PIL import Image

posts = []

@app.route('/') # decorators
# @app.route('/home')
def home():
    return render_template('home.html', posts=posts, isHome='active')

@app.route('/about')
def about():
    return render_template('about.html', title='About', isAbout='active')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = b.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash(f'Thank you for joining us {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and b.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            flash(f'Welcome {user.username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_file = random_hex + file_extension
    picture_path = os.path.join(app.root_path, 'static/pics', picture_file)
    
    i = Image.open(form_picture)
    i.thumbnail((128, 128))
    i.save(picture_path)

    return picture_file

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account is updated', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image = url_for('static', filename='pics/' + current_user.image)
    return render_template('account.html', title='Account', image=image, form=form)





