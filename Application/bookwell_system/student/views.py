from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from is_safe_url import is_safe_url
from flask import abort

import datetime

from . import student
from .. import db
from ..models import TimeSlotInventory, User, StaffCapability, SkillSet, Meeting, MeetingSlots, MeetingJoiners
from ..functions import flash_errors
from .forms import FormMeetingDetail

@student.route("/booking/step1")
def booking_step_1():
    skills = SkillSet.query.all()
    return render_template("/student/booking_1.html", skills=skills)

@student.route("/booking/step2")
def booking_step_2():
    skill_id = request.args.get("skill")
    staff = SkillSet.query.get(skill_id).staff
    public_meeting = Meeting.query.filter_by(skill=skill_id, allowJoining=True).all()
    return render_template("/student/booking_2.html", staff=staff, skill=skill_id, public_meeting=public_meeting)

    
@student.route("/booking/step3")
def booking_step_3():
    skill_id = request.args.get("skill")
    staff_id = request.args.get("staff")
    timeslots = TimeSlotInventory.query.filter_by(staff=staff_id, occupied=False).all()
    return render_template("/student/booking_3.html", timeslots=timeslots, skill=skill_id, staff=staff_id)

@student.route("/booking/step4")
def booking_step_4():
    skill_id = request.args.get("skill")
    staff_id = request.args.get("staff")
    timeslot_id = request.args.get("timeslot")
    skillset_verification = StaffCapability.query.filter_by(staff=staff_id, skill=skill_id).all()
    if not skillset_verification:
        flash("Invalid input, please retry.")
        return redirect(url_for("student.booking_step_1"))
    timeslot = TimeSlotInventory.query.get_or_404(timeslot_id)
    if timeslot.staff!=int(staff_id) or timeslot.occupied==True:
        flash("Timeslot has been taken or invalid input, please retry.")
        return redirect(url_for("student.booking_step_1"))
    timeslot.occupied=True
    new_meeting = Meeting(skill=skill_id, staff=staff_id)
    db.session.add(new_meeting)
    db.session.commit()
    new_meeting_slot = MeetingSlots(meeting=new_meeting.id, timeslot=timeslot_id)
    db.session.add(new_meeting_slot)
    meeting_joiner = MeetingJoiners(meeting=new_meeting.id, student=current_user.id)
    db.session.add(meeting_joiner)
    db.session.commit()
    flash("Your timeslot has been booked.")
    return redirect(url_for("student.booking_detail_edit", id=new_meeting.id))

@student.route("/booking/detail/edit", methods=["POST", "GET"])
def booking_detail_edit():
    meeting_id=request.args.get("id")
    meeting=Meeting.query.get_or_404(meeting_id)
    if meeting.owner!=current_user.id:
        flash("You have no access to modify this meeting.")
        return redirect(url_for("student.booking_detail", id=meeting_id))
    form=FormMeetingDetail()
    if request.method=='GET':
        form.allowJoining.data = meeting.allowJoining
        form.consentToRecording.data = meeting.consentToRecording
        form.topic.data = meeting.topic
        form.meetingPlace.data = meeting.meetingPlace
    if form.validate_on_submit():
        meeting.allowJoining=form.allowJoining.data
        meeting.consentToRecording = form.consentToRecording.data
        meeting.topic = form.topic.data
        meeting.meetingPlace = form.meetingPlace.data
        db.session.commit()
        flash("Detail has been saved.")
        return redirect(url_for("student.booking_detail", id=meeting_id))
    return render_template("/student/booking_edit_detail.html", form=form, meeting=meeting)

@student.route("/booking")
def booking_list():
    meetings=current_user.meetingjoiners
    return render_template("/student/booking_list.html", meetings=meetings)

@student.route("/booking/detail")
def booking_detail():
    meeting_id=request.args.get("id")
    meeting=Meeting.query.get_or_404(meeting_id)
    return render_template("/student/booking_detail.html", meeting=meeting, id=meeting_id)


@student.route("booking/join")
def booking_join():
    meeting_id=request.args.get("id")
    meeting = Meeting.query.get_or_404(meeting_id)
    validate = MeetingJoiners.query.filter_by(meeting=meeting_id, student=current_user.id).all()
    print(validate)
    if validate or meeting.allowJoining!=True:
        return abort(403)
    newLog = MeetingJoiners(meeting=meeting_id, student=current_user.id)
    db.session.add(newLog)
    db.session.commit()
    flash("You've registered for the meeting.")
    return redirect(url_for("student.booking_list"))