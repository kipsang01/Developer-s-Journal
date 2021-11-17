from flask import render_template,request,redirect,url_for,abort
from . import main
from .. import db,photos
from ..models import User,Journal,Note,Todo
from .forms import JournalForm,NotesForm
from flask_login import login_required,current_user




@main.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('index.html',todo_list=todo_list)


@main.route('/add-todo', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete = False)

    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('.index'))


@main.route('/update/<todo_id>')
def update_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('.index'))


@main.route('/delete/<todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('.index'))




@main.route('/create-journal', methods=['GET','POST'])
@login_required
def create_journal():
    form = JournalForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        journal = Journal(title=title, content=content,user_id=current_user.id)
        journal.save_journal()
        return redirect('.index')

    return render_template('create_journal.html', form=form,user=current_user)


@main.route('/journal/<post_id>/update',methods=['GET','POST'])
@login_required
def update_journal(journal_id):
    journal = Journal.query.get(journal_id)
    if journal.user != current_user:
        abort(403)

    form = JournalForm()
    if form.validate_on_submit():
        journal.title = form.title.data
        journal.content = form.content.data
        db.session.commit()
        return redirect(url_for('.index',id = journal.id))
    
    if request.method =='GET':
        form.title.data = journal.title
        form.content.data = journal.content

    return render_template('update_journal.html', form = form)