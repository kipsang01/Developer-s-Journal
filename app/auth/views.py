from flask import render_template,redirect,url_for,flash,request
from . import auth
from flask_login import login_user,logout_user,login_required
from ..models import User
from .forms import LoginForm,RegistrationForm
from .. import db


#Registration
@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        new_user.save_user()
        flash('Registered, you can now login', 'success')
        return redirect(url_for('auth.login'))
    title = "New Account"
    return render_template('auth/register.html',form = form,title=title)

#login
@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.home'))

        flash('Invalid username or Password','danger')

    title = "watchlist login"
    return render_template('auth/login.html',form = login_form,title=title)

#logout user
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out','success')
    return redirect(url_for("main.home"))