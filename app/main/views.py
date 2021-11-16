from flask import Flask
from .. import db,photos
from flask import render_template,request,redirect,url_for,abort,flash
from flask_login import login_required,current_user
from . import main
from sqlalchemy import  func, desc

@main.route('/')
@main.route('/home')
def home():
    pass
    return render_template('home.html')

@main.route('/about')
def about():
    pass
    return render_template('about.html')
