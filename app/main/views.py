

from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from .. import db,photos
from ..models import User,Journal,Note,Todo
from . forms import JournalForm, TodoForm,NotesForm
from flask_login import login_user,logout_user,login_required,current_user





@main.route('/',methods=['GET', 'POST'])
def home():
    journals = Journal.get_journals()
    form = TodoForm()
    todos = Todo.query.all()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            new_todo = Todo(title=title, complete = False)
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for('.home'))
            
    
    return render_template('base.html', form=form, todos=todos, journals= journals)



@main.route('/add-journal', methods=['GET', 'POST'])
@login_required
def add_journal():
    form = JournalForm()
    if request.method=='POST':
        if form.validate_on_submit:
            title = form.title.data
            content = form.content.data
            category = form.category.data
            new_journal = Journal(title = title, content = content, category = category,user_id = current_user.id)
            new_journal.save_journal()
            return redirect(url_for('.home'))
    return render_template('add-journal.html', form =form)



@main.route('/journal/<journal_id>/update',methods=['GET','POST'])
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

        return redirect(url_for('.home'))
    
    if request.method =='GET':
        form.title.data = journal.title
        form.content.data = journal.content


    return render_template('add-journal.html', form = form)



@main.route('/create-notes/<journal_id>', methods = ['GET','POST'])
@login_required
def create_notes(journal_id):

    form = NotesForm()
    journal = Journal.query.filter_by(id=journal_id).first()

    if not journal:
        abort(404)

    if form.validate_on_submit():
        notes = form.notes.data

        new_note = Note(notes=notes,user_id=current_user.id,journal_id=journal.id)
        new_note.save_notes()
        return redirect(url_for('.journal', id=journal.id))

    return render_template('create_notes.html',form = form)


@main.route('/<journal_id>/delete', methods=['POST','GET'])
def delete_journal(journal_id):
    journal = Journal.query.filter_by(id=journal_id).first()
    db.session.delete(journal)
    db.session.commit()
    flash('Deleted successfully','danger')
    return redirect(url_for('.home'))



@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/profile')
def profile():
    return render_template('profile/profile.html')

@main.route('/<username>/journals')
def user_journals(username):
    journals = User.query.filter_by(username=username).all()
    return render_template('journals.html', journals=journals)


@main.route('/add-todo', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete = False)

    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for('.home'))


@main.route('/update/<todo_id>')
def update_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()

    return redirect(url_for('.home'))


@main.route('/todo/delete/<todo_id>', methods=['POST','GET'])
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    flash('Deleted successfully','danger')
    return redirect(url_for('.home'))
