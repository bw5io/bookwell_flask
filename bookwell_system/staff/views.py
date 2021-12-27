from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from is_safe_url import is_safe_url

from . import staff
from .. import db
from ..models import User, StaffCapability, SkillSet
# from .forms import RegistrationForm, LoginForm

@staff.route("/skills")
def skill_list_view():
    skills=SkillSet.query.all()
    current_skills=StaffCapability.query.filter_by(staff=current_user.id).all()
    current_skill_list=[x.skill for x in current_skills]
    return render_template('staff/skills.html', title='Skill Selection', skills=skills, current=current_skill_list)

@staff.route("/skills/toggle")
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