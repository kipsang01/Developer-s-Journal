from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,RadioField,TextAreaField
from wtforms.fields.simple import BooleanField
from wtforms.validators import InputRequired, Email


class JournalForm(FlaskForm):
    title =  StringField('Enter here the title..',validators = [InputRequired()])
    content = TextAreaField('Enter  here the content..',validators = [InputRequired()])
    category = BooleanField('Private')
    submit = SubmitField('Submit')
    
    
class TodoForm(FlaskForm):
    title =  StringField('Title:',validators = [InputRequired()])
    submit=SubmitField('submit')
    
