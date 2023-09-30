from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, AnyOf


class AddPetForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])

    species = SelectField("Species",
                          choices=[('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')],
                          validators=[InputRequired()])
    
    photo_url = StringField("Photo Url", validators=[Optional(), URL()])

    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=30, message='Age must be between 0 and 30')])

    notes = TextAreaField("Notes")

    available = BooleanField("Pet is available")

