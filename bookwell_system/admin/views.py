from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import admin
from .. import db
from ..models import SkillSet
from .forms import *

@admin.route('/list')
def skill_list_view():
    skills=SkillSet.query.all()
    form=FormAddSkillSet()
    return render_template("admin/skill/list.html", skills=skills, form=form)

@admin.route('/list/create', methods=['POST'])
def skill_list_create():
    form=FormAddSkillSet()
    if form.validate_on_submit():
        skill=SkillSet(skill=form.skill.data)
        db.session.add(skill)
        db.session.commit()
        print("Skill Set Added")
    else:
        print("Error")
    return redirect(url_for('admin.skill_list_view'))

@admin.route('/list/delete/<int:id>')
def skill_list_delete(id):
    skill=SkillSet.query.get_or_404(id)
    print(f"{skill.skill} in Deletion")
    SkillSet.query.filter_by(id=skill.id).delete(synchronize_session=False)
    db.session.commit()
    print("Deleted.")
    return redirect(url_for('admin.skill_list_view'))