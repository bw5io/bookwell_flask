from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired
from ..models import SkillSet, User
from flask import flash

class FormAddSkillSet(FlaskForm):
    skill = StringField('Name of Skill', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_skill(self, skill):
        skillExist=SkillSet.query.filter_by(skill=skill.data).first()
        if skillExist:
            raise ValidationError(message='Skill already exists.')