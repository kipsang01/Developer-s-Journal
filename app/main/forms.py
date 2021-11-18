from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField,BooleanField
from wtforms.validators import InputRequired



class NotesForm(FlaskForm):
    '''
    Class to create a wtf form for creating a pitch
    '''
    notes = TextAreaField('Notes',validators=[InputRequired()])
    submit = SubmitField('Submit')


class JournalForm(FlaskForm):
    title =  StringField('Enter here the title..',validators = [InputRequired()])
    content = TextAreaField('Enter  here the content..',validators = [InputRequired()])
    category = BooleanField('Private')
    submit = SubmitField('Submit')
    
    
class TodoForm(FlaskForm):
    title =  StringField('Title:',validators = [InputRequired()])
    submit=SubmitField('submit')
