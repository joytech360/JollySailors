from app import app, db
import random
import jwt

from flask import render_template, url_for, flash, redirect, request
from app.forms import LoginForm, RegistrationForm, TwoFactorAuthForm, DaycareRegistrationForm, AddChildForm, ChildRequestForm
from app.models import User, Daycare, Child, DaycareStudent, ChildRequest
from app.email import send_registration_confirmation_email, email_user
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFError
from sqlalchemy import func
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from time import time as ttime
from datetime import datetime, timedelta, time


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    next = request.referrer
    if current_user.is_authenticated:
        logout_user()
    flash(f'{e.description}', 'alert-warning')
    return redirect(next)


# to add datetime in jinja templates
@app.context_processor
def inject_datetime_now():
    return {'datetime_now': datetime.now()}


@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js'), 200, {'Content-Type': 'text/javascript', 'Service-Worker-Allowed': '/'}


@app.route('/brand_logo')
def brand_logo():
    return app.send_static_file('brand_logo.png')


@app.route('/brand_icon')
def brand_icon():
    return app.send_static_file('brand_icon.ico')


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return redirect(url_for('parent'))#render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        email=reg_form.email.data.lower().replace(' ', '')
        user_q = User.query.filter(func.lower(User.email) == email).all()
        if user_q:
            flash('The email is already in use!', 'alert-warning')
            return redirect(url_for('login'))
        user = User(name=reg_form.name.data, email=email)
        user.set_password(reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Thank you for registering. You may now be able to log into your account.", 'alert-info')
        return redirect(url_for('login'))
    return render_template('register.html', reg_form=reg_form)

@app.route('/admin_apply', methods=['GET', 'POST'])
def admin_apply():
    if current_user.is_daycare_admin:
        return redirect(url_for('index'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        email=reg_form.email.data.lower().replace(' ', '')
        user_q = User.query.filter(func.lower(User.email) == email).all()
        if user_q:
            flash('The email is already in use!', 'alert-warning')
            return redirect(url_for('login'))
        user = User(name=reg_form.name.data, email=email)
        user.set_password(reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Thank you for registering. You may now be able to log into your account.", 'alert-info')
        return redirect(url_for('login'))
    return render_template('register.html', reg_form=reg_form)

@app.route('/register_user/two_factor_authentication/<token>', methods=['GET', 'POST'])
def register_user_2fa(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = TwoFactorAuthForm()
    if form.validate_on_submit():
        try:
            user_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['data']
        except:
            flash('Invalid token!', 'alert-warning')
            return redirect(url_for('login'))
        if not user_token['two_factor_auth_code'] == form.code.data:
            flash('Invalid token!', 'alert-warning')
            return redirect(url_for('login'))
        user_q = User.query.filter(func.lower(User.email) == user_token['email'].lower()).all()
        if user_q:
            flash('The email is already in use!', 'alert-warning')
            return redirect(url_for('login'))
        user = User(name=user_token['name'],
                    email=user_token['email'])
        user.set_password(user_token['password'])
        db.session.add(user)
        db.session.commit()

        flash("Thank you for registering. You may now be able to log into your account.", 'alert-info')
        return redirect(url_for('login'))
    return render_template('two_factor_auth.html', form=form)


@app.route('/register_user/<token>', methods=['GET', 'POST'])
def register_user(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    try:
        user_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['data']
    except:
        flash('Invalid token!', 'alert-warning')
        return redirect(url_for('login'))

    user_q = User.query.filter(func.lower(User.email) == user_token['email'].lower()).all()
    if user_q:
        flash('The email is already in use!', 'alert-warning')
        return redirect(url_for('login'))
    user = User(name=user_token['name'],
                email=user_token['email'])
    user.set_password(user_token['password'])
    db.session.add(user)
    db.session.commit()
    flash("Thank you for registering. You may now be able to log into your account.", 'alert-info')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.email) == form.email.data.replace(' ', '').lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'alert-warning')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=form.remember_me.data)
            db.session.commit()
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register_daycare', methods=['GET', 'POST'])
@login_required
def register_daycare():
    form = DaycareRegistrationForm()
    if form.validate_on_submit():
        daycare = Daycare(name=form.name.data,
                          email=form.email.data,
                          phone_no=form.phone.data,
                          street=form.street.data,
                          city=form.city.data,
                          province=form.province.data,
                          country='Canada',
                          capacity=form.capacity.data,
                          opening_time=form.opening_time.data,
                          closing_time=form.closing_time.data
                          )
        db.session.add(daycare)
        db.session.commit()
        daycare.staffs.append(current_user)
        db.session.commit()
        flash(f'{daycare.name} has been registered')
        return redirect(url_for('daycare', id=daycare.id, name=daycare.name))
    return render_template('daycare_registration.html', form=form)


@app.route('/my_daycare')
@login_required
def my_daycare():
    daycare = current_user.my_daycare()
    return render_template('daycare.html', daycare=daycare)


@app.route('/daycare/<int:id>/<string:name>', methods=['GET', 'POST'])
@login_required
def daycare(id: int, name: str):
    daycare = Daycare.query.get(id)
    form = ChildRequestForm()
    form.child.choices = [(0, 'Select Child')] + [(i.id, f"{i.name}") for i in current_user.children]
    if form.validate_on_submit():
        child_request = ChildRequest(daycare_id=daycare.id,
                                     child_id=form.child.data,
                                     message=form.message.data)
        db.session.add(child_request)
        db.session.commit()
        flash('Child request has been submitted', 'alert-info')
    return render_template('daycare.html', daycare=daycare, form=form)


@app.route('/daycare_registry')
@login_required
def daycare_registry():
    daycares = Daycare.query.all()
    return render_template('daycare_registry.html', daycares=daycares)


@app.route('/parent', methods=['GET', 'POST'])
@login_required
def parent():
    form = AddChildForm()
    if form.validate_on_submit():
        child = Child(name=form.name.data,
                      birth_date=form.dob.data,
                      parent_id=current_user.id)
        db.session.add(child)
        db.session.commit()
        flash(f'Child {child.name} has been added', 'alert-info')
    return render_template('parent.html', form=form)

#
# @app.route('/add_child_request/<int:id>/<string:name>')
# @login_required
# def add_child_request(id: int, name: str):
#     daycare = Daycare.query.get(id)
#     form = ChildRequestForm()
#     form.child.choices = [(0, 'Select Child')] + [(i.id, f"{i.name}") for i in current_user.children]
#     if form.validate_on_submit():
#         child_request = ChildRequest(daycare_id=daycare.id,
#                                      child_id=form.child.id,
#                                      message=form.message.data)
#         db.session.add(child_request)
#         db.session.commit()
#     return render_template('add_child_request.html', form=form)


@app.route('/approve_child_request/<int:daycare_id>/<int:child_id>', methods=['GET', 'POST'])
@login_required
def approve_child_request(daycare_id: int, child_id: int):
    daycare = Daycare.query.get(daycare_id)
    child = Child.query.get(child_id)
    child = DaycareStudent(daycare_id=daycare_id, child_id=child_id, date_joined=datetime.now())
    db.session.add(child)
    db.session.commit()
    daycare_requests = ChildRequest.query.filter_by(child_id=child.id).all()
    for daycare in daycare_requests:
        db.session.delete(daycare)
        db.session.commit()
    flash(f'Child {child.child.name} has been accepted', 'alert-info')
    return redirect(url_for('daycare', id=daycare.id, name=daycare.name))
