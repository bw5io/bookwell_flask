from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    user_type = db.Column(db.Integer, nullable=False, default=0)

    skill = db.relationship('StaffCapability',backref='User',lazy=True)
    timeslots = db.relationship('TimeSlotInventory', lazy=True)
    meetingjoiners = db.relationship('MeetingJoiners', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

class SkillSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(100), nullable=False)

    staff = db.relationship('StaffCapability',backref='SkillSet',lazy=True)
    meetings = db.relationship('Meeting',backref='SkillSet', lazy=True)

    def __repr__(self):
        return f"Skill Set('{self.skill}')"

class StaffCapability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    skill = db.Column(db.Integer, db.ForeignKey("skill_set.id", ondelete="CASCADE"), nullable=False)
    
class TimeSlotInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    startTime = db.Column(db.Time, nullable=False)
    endTime = db.Column(db.Time, nullable=False)
    occupied = db.Column(db.Boolean, nullable=False, default=False)

    meetingSlots = db.relationship('MeetingSlots', lazy=True, backref="slotinfo")

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    skill = db.Column(db.Integer, db.ForeignKey("skill_set.id"), nullable=False)
    meetingPlace = db.Column(db.String(500))
    topic = db.Column(db.String(500))
    allowJoining = db.Column(db.Boolean, nullable=False, default=False)
    consentToRecording = db.Column(db.Boolean, nullable=False, default=False)
    owner = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    
    meetingSlots = db.relationship('MeetingSlots', lazy=True, backref="Meeting")
    meetingJoiners = db.relationship('MeetingJoiners', lazy=True, backref="Meeting")
    ownerUser = db.relationship('User', backref='ownedMeetings', foreign_keys=[owner])
    staffUser = db.relationship('User', backref='staffMeetings', foreign_keys=[staff])

class MeetingSlots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting = db.Column(db.Integer, db.ForeignKey("meeting.id", ondelete="CASCADE"), nullable=False)
    timeslot = db.Column(db.Integer, db.ForeignKey("time_slot_inventory.id"), nullable=False)

class MeetingJoiners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting = db.Column(db.Integer, db.ForeignKey("meeting.id", ondelete="CASCADE"), nullable=False)
    student = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

