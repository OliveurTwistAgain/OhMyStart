# flaskstarter/settings/views.py

# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..extensions import db
from ..user import Users
from .forms import ProfileForm, PasswordForm

settings = Blueprint('settings', __name__, url_prefix='/settings')

@settings.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = Users.query.filter_by(email=current_user.email).first_or_404()
    form = ProfileForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('Profile Changes Saved!', 'success')

    return render_template('settings/profile.html', user=user, active="profile", form=form)

@settings.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    user = Users.query.filter_by(email=current_user.email).first_or_404()
    form = PasswordForm()

    if form.validate_on_submit():
        if user.check_password(form.password.data):  # Vérifiez si l'ancien mot de passe est correct
            user.password = form.new_password.data
            db.session.commit()
            flash('Password updated.', 'success')
            return redirect(url_for('settings.profile'))
        else:
            flash('Current password is incorrect.', 'danger')

    return render_template('settings/password.html', user=user, active="password", form=form)
