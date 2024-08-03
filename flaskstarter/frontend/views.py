# flaskstarter/frontend/views.py

# -*- coding: utf-8 -*-

from uuid import uuid4
from itsdangerous import URLSafeSerializer
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect)
from flask_login import (login_required, login_user, current_user,
                         logout_user, login_fresh)

from ..user import Users, ACTIVE
from ..extensions import db, login_manager
from .forms import (SignupForm, LoginForm, RecoverPasswordForm,
                    ChangePasswordForm, ContactUsForm, LieuForm)
from .models import ContactUs, Lieu
from ..emails import send_async_email

frontend = Blueprint('frontend', __name__)

@frontend.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.dashboard'))

    query = request.args.get('q', '')  # Récupère le terme de recherche depuis la query string
    results = []

    if query:
        # Rechercher les lieux par nom (ou d'autres caractéristiques)
        results = Lieu.query.filter(Lieu.name.ilike(f'%{query}%')).all()

    # Autres lieux à afficher, si besoin
    lieux = Lieu.query.limit(10).all()  # Exemples de lieux
    city = "une ville"  # Remplacer par la ville réelle ou ajuster selon vos besoins

    return render_template('frontend/landing.html', _active_home=True, results=results, query=query, lieux=lieux, city=city)

@frontend.route('/lieux')
def lieux():
    lieux = Lieu.query.all()
    return render_template('frontend/lieux.html', lieux=lieux)

@frontend.route('/lieux/add', methods=['GET', 'POST'])
@login_required
def add_lieu():
    form = LieuForm()

    if form.validate_on_submit():
        lieu = Lieu(
            name=form.name.data,
            description=form.description.data,
            location=form.location.data,
            image_url=form.image_url.data
        )
        db.session.add(lieu)
        db.session.commit()
        flash('Lieu ajouté avec succès!', 'success')
        return redirect(url_for('frontend.lieux'))

    return render_template('frontend/add_lieu.html', form=form)

@frontend.route('/lieux/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_lieu(id):
    lieu = Lieu.query.get_or_404(id)
    form = LieuForm(obj=lieu)

    if form.validate_on_submit():
        lieu.name = form.name.data
        lieu.description = form.description.data
        lieu.location = form.location.data
        lieu.image_url = form.image_url.data
        db.session.commit()
        flash('Lieu modifié avec succès!', 'success')
        return redirect(url_for('frontend.lieux'))

    return render_template('frontend/edit_lieu.html', form=form, lieu=lieu)

@frontend.route('/lieux/delete/<int:id>', methods=['POST'])
@login_required
def delete_lieu(id):
    lieu = Lieu.query.get_or_404(id)
    db.session.delete(lieu)
    db.session.commit()
    flash('Lieu supprimé avec succès!', 'success')
    return redirect(url_for('frontend.lieux'))

@frontend.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    form = ContactUsForm()
    if form.validate_on_submit():
        _contact = ContactUs()
        form.populate_obj(_contact)
        db.session.add(_contact)
        db.session.commit()
        flash('Thanks! We\'ll get back to you shortly!', 'success')
        return redirect(url_for('frontend.contact_us'))
    return render_template('frontend/contact_us.html', form=form)

@frontend.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.index'))
    form = LoginForm(login=request.args.get('login', None), next=request.args.get('next', None))
    if form.validate_on_submit():
        user, authenticated = Users.authenticate(form.login.data, form.password.data)
        if user and authenticated:
            if user.status_code != 2:
                flash("Please verify your email address to continue", "danger")
                return redirect(url_for('frontend.login'))
            remember = request.form.get('remember') == 'y'
            if login_user(user, remember=remember):
                flash("Logged in", 'success')
            return redirect(form.next.data or url_for('frontend.index'))
        else:
            flash('Sorry, invalid login', 'danger')
    return render_template('frontend/login.html', form=form, _active_login=True)

@frontend.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('frontend.index'))

@frontend.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.dashboard'))
    form = SignupForm(next=request.args.get('next'))
    if form.validate_on_submit():
        user = Users()
        user.status_code = 2
        user.account_type = 0
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        confirm_user_mail(form.name.data, form.email.data)
        flash(u'Confirmation email sent to ' + form.email.data + ' Please verify!', 'success')
        return redirect(url_for('frontend.login'))
    return render_template('frontend/signup.html', form=form, _active_signup=True)

def confirm_user_mail(name, email):
    s = URLSafeSerializer('your-secret-key')  # Modifiez ceci pour une clé sécurisée
    key = s.dumps([name, email])
    subject = 'Confirm your account for ' + current_app.config['PROJECT_NAME']
    url = url_for('frontend.confirm_account', secretstring=key, _external=True)
    html = render_template('macros/_confirm_account.html', project=current_app.config['PROJECT_NAME'], url=url)
    send_async_email(subject, html, email)

@frontend.route('/confirm_account/<secretstring>', methods=['GET', 'POST'])
def confirm_account(secretstring):
    s = URLSafeSerializer('your-secret-key')  # Modifiez ceci pour une clé sécurisée
    uname, uemail = s.loads(secretstring)
    user = Users.query.filter_by(name=uname).first()
    if user:
        user.status_code = ACTIVE
        db.session.add(user)
        db.session.commit()
        flash(u'Your account was confirmed successfully!!!', 'success')
    else:
        flash(u'Invalid confirmation link', 'danger')
    return redirect(url_for('frontend.login'))

@frontend.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if current_user.is_authenticated:
        if not login_fresh():
            return redirect(url_for('frontend.login'))
    form = ChangePasswordForm(email_activation_key=request.values.get("email_activation_key"), email=request.values.get("email"))
    if form.validate_on_submit():
        update_password(form.email.data, form.email_activation_key.data, form.password.data)
        flash(u"Your password has been changed, log in again", "success")
        return redirect(url_for("frontend.login"))
    return render_template("frontend/change_password.html", form=form)

def update_password(email, email_activation_key, password):
    user = Users.query.filter(Users.email.ilike(email), email_activation_key=email_activation_key).first()
    if user:
        user.password = password
        user.email_activation_key = None
        db.session.add(user)
        db.session.commit()
        flash(u"Your password was updated", "success")

@frontend.route('/dashboard')
@login_required
def dashboard():
    return render_template('frontend/dashboard.html')

@frontend.route('/profile')
@login_required
def profile():
    return render_template('frontend/profile.html')
