from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import SubmitField, IntegerField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, ValidationError
from ..models import TimeSlotInventory
from ..functions import Compare
from flask import flash
import datetime

class FormAddTimeSlot(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired(), Compare("end_time", message="End time should be later than Start time.", direction="right")])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def validate_date(self, date):
        if date.data<=datetime.date.today():
            raise ValidationError("Date should be later than today.")
        data=TimeSlotInventory.query.filter_by(staff=current_user.id, date=date.data).first()
        if data:
            raise ValidationError("Time slots have already been created for that date.")

class FormActualTime(FlaskForm):
    actual_time = IntegerField("Actual Time")
    submit = SubmitField('Submit')