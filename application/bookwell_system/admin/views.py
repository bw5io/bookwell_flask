from datetime import datetime, timedelta
from operator import and_
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import admin
from .. import db
from ..models import SkillSet, Permission, TimeSlotInventory
from .forms import *
from ..functions import flash_errors, get_week
from ..decorators import permission_required


@admin.route('/skill')
@permission_required(Permission.ADMIN)
def skill_list_view():
    skills=SkillSet.query.all()
    form=FormAddSkillSet()
    return render_template("admin/skill/list.html", skills=skills, form=form)


@admin.route('/skill/create', methods=['POST'])
@permission_required(Permission.ADMIN)
def skill_list_create():
    form=FormAddSkillSet()
    if form.validate_on_submit():
        skill=SkillSet(skill=form.skill.data)
        db.session.add(skill)
        db.session.commit()
        print("Skill Set Added")
    else:
        flash_errors(form)
    return redirect(url_for('admin.skill_list_view'))

@admin.route('/skill/delete/<int:id>')
@permission_required(Permission.ADMIN)
def skill_list_delete(id):
    skill=SkillSet.query.get_or_404(id)
    print(f"{skill.skill} in Deletion")
    SkillSet.query.filter_by(id=skill.id).delete(synchronize_session=False)
    db.session.commit()
    print("Deleted.")
    return redirect(url_for('admin.skill_list_view'))

class stat_occupied_or_not:
    count = 0
    occupied = 0
    def __repr__(self):
        return f"All: {self.count}, Occupied: {self.occupied}"

@admin.route('/dashboard')
@permission_required(Permission.ADMIN)
def dashboard_view():
    try:
        day = datetime.strptime(request.args.get('date'),"%d-%m-%Y") if request.args.get('date') else datetime.now()+timedelta(days=7)
    except:
        day = datetime.now()+timedelta(days=7)
    start_date, end_date = get_week(day)
    this_week_slots=TimeSlotInventory.query.filter(and_(TimeSlotInventory.date>=start_date, TimeSlotInventory.date<= end_date)).all()
    by_date, by_staff = {}, {}
    for i in this_week_slots:
        if i.date not in by_date:
            by_date[i.date]=stat_occupied_or_not()
        by_date[i.date].count+=1
        by_date[i.date].occupied+=i.occupied
        if i.staff not in by_staff:
            by_staff[i.staff]=stat_occupied_or_not()
        by_staff[i.staff].count+=1
        by_staff[i.staff].occupied+=i.occupied
    return str(by_date) + str(by_staff) + "\n" + str(day)
            
            
