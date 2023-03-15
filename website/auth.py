from flask import Blueprint, redirect, render_template, redirect, url_for, request, flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in succefully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('Email does\'nt exist', category='error')

    return render_template("logging.html", user=current_user)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
    
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            message = flash('Email must be graeter than 4 characters', category='error')
        elif len(first_name) < 3:
            message = flash('First name must be grater than 3 characters', category='error')
        elif password1 != password2:
            message = flash('Passwords must be the same', category='error')
        elif len(password1) < 7:
            message = flash('Password must be greater then 7 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash('Account created!', category='succes')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)