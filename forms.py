from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, validators, TextAreaField


class DataForm(FlaskForm):
    message = StringField('Data', [validators.Required()])
    last_message = TextAreaField('LastMessage', default="add")
    submit = SubmitField('Submit')

class newForm(FlaskForm):
    message = TextAreaField('message')
    submit = SubmitField('Submit')

class lectureForm(FlaskForm):
    msg = TextAreaField(id=1,default="hi",_name="1")

    def append_field(cls, name, field):
        setattr(cls, name, field)
        return cls
