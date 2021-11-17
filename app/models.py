from sqlalchemy.orm import backref
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from flask import abort

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(200),index = True)
    email = db.Column(db.String(200),unique = True,index = True)
    about = db.Column(db.String(200))
    profile_pic_path = db.Column(db.String)
    password_hash = db.Column(db.String(200))
    journals = db.relationship('Journal',backref='user',lazy='dynamic')
    notes= db.relationship('Note',backref='user',lazy='dynamic')
    def save_user(self):
        db.session.add(self)
        db.session.commit()
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'


class Journal(db.Model):
    __tablename__ = 'journals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category = db.Column(db.Boolean)
    time = db.Column(db.DateTime(timezone = True), default=datetime.now)
    notes = db.relationship('Note',backref='journal',lazy='dynamic', cascade="all, delete"  )

    def save_journal(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_journal(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_journals(cls):
        journals = Journal.query.all()
        if journals is None:
            abort(404)
        return journals
    
    


    def __repr__(self):
        return f'Journal {self.title}'


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(255))
    time = db.Column(db.DateTime(timezone = True), default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    journal_id = db.Column(db.Integer, db.ForeignKey('journals.id'))

    def save_notes(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_notes(self,id):
        notes = Note.query.order_by(Note.time.desc()).filter_by(journal_id=id).all()
        return notes

    def __repr__(self):
        return f'notes:{self.notes}'


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

    def save_todos(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_todos(cls):
        todos = Todo.query.all()
        return todos


    def __repr__(self):
        return f'Todo {self.title}'