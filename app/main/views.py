
from flask import render_template,request,redirect,url_for,abort
from . import main
from .. import db,photos
from ..models import User,Journal,Note,Todo




@main.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('base.html',todo_list=todo_list)


@main.route('/add-todo', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete = False)

    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))


@main.route('/update/<todo_id>')
def update_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))


@main.route('/delete/<todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

