from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from is_safe_url import is_safe_url
from flask import abort

import datetime

from ..decorators import permission_required
from .forms import FormActualTime, FormAddTimeSlot

from . import staff
from .. import db
from ..models import Permission, TimeSlotInventory, User, StaffCapability, SkillSet, Meeting
from ..functions import flash_errors

@staff.route("/skills")
@permission_required(Permission.STAFF)
def skill_list_view():
    skills=SkillSet.query.all()
    current_skills=StaffCapability.query.filter_by(staff=current_user.id).all()
    current_skill_list=[x.skill for x in current_skills]
    return render_template('staff/skills.html', title='Skill Selection', skills=skills, current=current_skill_list)

@staff.route("/skills/toggle")
@permission_required(Permission.STAFF)
def skill_list_toggle():
    next=request.args.get('skill')
    skill=StaffCapability.query.filter_by(staff=current_user.id, skill=next)
    if skill.all():
        skill.delete(synchronize_session=False)
        print("Deleted")
    else:
        skill=StaffCapability(staff=current_user.id, skill=next)
        db.session.add(skill)
        print("Added")
    db.session.commit()
    return redirect(url_for("staff.skill_list_view"))

@staff.route("/timeslot")
@permission_required(Permission.STAFF)
def timeslot_view():
    timeslots=TimeSlotInventory.query.filter_by(staff=current_user.id)
    meetings=Meeting.query.filter_by(staff=current_user.id)
    return render_template('staff/timeslot.html', title='Time Slot Management', timeslots=timeslots, meetings=meetings)

@staff.route("/timeslot/create", methods=["POST", "GET"])
@permission_required(Permission.STAFF)
def timeslot_create():
    form=FormAddTimeSlot()
    if form.validate_on_submit():
        delta=datetime.timedelta(minutes=15)
        current=datetime.time(hour=form.start_time.data.hour, minute=15*(form.start_time.data.minute//15))
        consecutive=0
        while current<form.end_time.data:
            if consecutive<=7:
                new_slot = TimeSlotInventory(staff=current_user.id, date=form.date.data, startTime=current, endTime=(datetime.datetime.combine(datetime.date.today(), current)+delta).time())
                db.session.add(new_slot)
                db.session.commit() 
                consecutive+=1
            else:
                consecutive=0
            current=(datetime.datetime.combine(datetime.date.today(), current)+delta).time()
        return redirect(url_for("staff.timeslot_view"))
    else:
        flash_errors(form)
    return render_template('staff/timeslot_create.html', title='Time Slot Creation', form=form)

@staff.route("/timeslot/delete")
@permission_required(Permission.STAFF)
def timeslot_delete():
    id=request.args.get('id')
    slot=TimeSlotInventory.query.get_or_404(id)
    if slot.staff!=current_user.id:
        return abort(401)
    print(f"Timeslot in Deletion")
    TimeSlotInventory.query.filter_by(id=id).delete(synchronize_session=False)
    db.session.commit()
    print("Deleted.")
    flash("Timeslot deleted.")
    return redirect(url_for('staff.timeslot_view'))

@staff.route("/timeslot/detail")
@permission_required(Permission.STAFF)
def timeslot_detail():
    form=FormActualTime()
    meeting_id=request.args.get("id")
    meeting=Meeting.query.get_or_404(meeting_id)
    return render_template("staff/meeting_detail.html", meeting=meeting, id=meeting_id, form=form)

@staff.route("/timeslot/actualtime", methods=["POST"])
@permission_required(Permission.STAFF)
def timeslot_actual_time_input():
    form=FormActualTime()
    id=request.args.get('id')
    meeting=Meeting.query.get_or_404(id)
    if meeting.staff!=current_user.id:
        abort(403)
    if form.validate_on_submit():
        meeting.actualTime=form.actual_time.data
        db.session.commit()
        flash("Actual time updated.")
    return redirect(url_for('staff.timeslot_detail', id=id))