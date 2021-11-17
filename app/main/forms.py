from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField,BooleanField
from wtforms.validators import Required



class JournalForm(FlaskForm):
    '''
    Class to create a wtf form for creating a pitch
    '''
    title = TextAreaField('Title',validators=[Required()])
    content = TextAreaField('Post',validators=[Required()])
    remember = BooleanField('Private')
    submit = SubmitField('Submit')


class NotesForm(FlaskForm):
    '''
    Class to create a wtf form for creating a pitch
    '''
    notes = TextAreaField('Notes',validators=[Required()])
    submit = SubmitField('Submit')