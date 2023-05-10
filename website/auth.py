from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from functools import wraps

from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

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
                session['login_required']= True
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
                # return  render_template('dashboard.html')   
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user =current_user) 

# Decorator  check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            flash('Unothorized, please login', 'danger')
            return redirect(url_for('auth.login'))
    return wrap  

@auth.route('/logout')
# @is_logged_in
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))
    
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        firstname = request.form['firstname']
        secondname = request.form['secondname']
        idn = request.form['idn']
        phonenumber = request.form['phonenumber']
        registerdate= datetime.now()
        country = request.form['country']
        village = request.form['village']
        sizeofland = request.form['sizeofland']
        password1 = request.form['password1']
        password2 = request.form['password2']

        user = User.query.filter_by(email=email).first()

        if user:
            flash('this email already exist', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstname)<2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, firstname=firstname, secondname=secondname, idn=idn,registerdate=registerdate , phonenumber=phonenumber,country=country, village=village, sizeofland=sizeofland, password =generate_password_hash(
                password1, method='sha256')) 
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            return redirect(url_for('views.dashboard'))
    return  render_template('register.html', user=current_user)
