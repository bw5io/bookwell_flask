from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired
from ..models import TimeSlotInventory
from ..functions import Compare
from flask import flash
import datetime

class FormMeetingDetail(FlaskForm):
    topic = StringField('Topic')
    meetingPlace = StringField('Meeting URL (Zoom/Teams/etc)')
    allowJoining = BooleanField('Allow other students to join')
    consentToRecording = BooleanField('Allow recording for the session')
    submit = SubmitField('Submit')