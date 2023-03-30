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


@app.route('/register_daycare')
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


@app.route('/daycare/upload_centres')
def upload_centres():
    centres = [{'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'Regina Open Door Society Child Care Centre', 'address': '1855 Smith Street, Regina, SK, S4P 2N5 (Downtown)', 'phone': '306-545-3873', 'lat': 50.449499, 'lng': -104.6148778}, {'type': 'Centre', 'name': 'YWCA Child Care Centre', 'address': '1940 McIntyre Street, Regina, SK, S4P 2R3 (Downtown)', 'phone': '306-525-2141', 'lat': 50.4480557, 'lng': -104.6169768}, {'type': 'Centre', 'name': "YWCA Family Children's Centre", 'address': '1940 McIntyre Street, Regina, SK, S4P 2R3 (Downtown)', 'phone': '306-525-2141', 'lat': 50.4480557, 'lng': -104.6169768}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'YMCA Child Care Centre', 'address': '2400 – 13th Avenue, Regina, SK, S4P 0V9 (Downtown)', 'phone': '306-757-9622', 'lat': 50.4460012, 'lng': -104.615945}, {'type': 'Accepts infants 6 weeks - 18 months', 'name': 'Green Earth Daycare', 'address': '1632 Angus Street, Regina, SK, S4T 1Z2', 'phone': '306-543-0011', 'lat': 50.4527031, 'lng': -104.6199209}, {'type': 'Centre', 'name': 'Cathedral Area Cooperative Daycare', 'address': '2051 Cameron Street, Regina, SK, S4T 2V4 (Cathedral)', 'phone': '306-522-7533', 'lat': 50.446169, 'lng': -104.6251181}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'Stepping Stones, Robinson', 'address': '1501 Robinson Street, Regina, SK, S4T 2N9 (North Central)', 'phone': '306-352-3755', 'lat': 50.4546797, 'lng': -104.623722}, {'type': 'Centre', 'name': "The Dragon's Den Child Care", 'address': '2401 Retallack Street, Regina, SK, S4T 2L2 (Crescents)', 'phone': '306-791-8682', 'lat': 50.4404146, 'lng': -104.6218507}, {'type': 'Home', 'name': 'Samreen Khan', 'address': '1409 Rae Street, Regina, SK, S4T 2C6', 'phone': '306-580-4948', 'lat': 50.4565445, 'lng': -104.6207594}, {'type': 'Home', 'name': 'Crystal Benjamin', 'address': '2345 Toronto Street, Regina, SK, S4P 1N6', 'phone': '306-698-3226', 'lat': 50.4415367, 'lng': -104.5994292}, {'type': 'Centre, Teen parent infant centre, Accepts infants 6 weeks - 18 months', 'name': 'MacKenzie Infant Care Centre (Registered Balfour Students only)', 'address': '1308 College Avenue, Regina, SK, S4P 1B2 (General Hospital Area)', 'phone': '306-569-1308', 'lat': 50.44107409999999, 'lng': -104.5995856}, {'type': 'Centre', 'name': 'Little Memories Child Care Co-op', 'address': '3128 Dewdney Avenue, Regina, SK, S4T 0Y5 (North Central)', 'phone': '306-522-0393', 'lat': 50.4553916, 'lng': -104.6261199}, {'type': 'Centre, Teen parent infant centre, Accepts infants 6 weeks - 18 months', 'name': 'Mackenzie Infant Care Centre-Balfour Site II (Registered Balfour Students only)', 'address': '1245 College Avenue, Regina, SK, S4P 1B1 (General Hospital Area)', 'phone': '306-569-1308', 'lat': 50.44007389999999, 'lng': -104.5990872}, {'type': 'Centre', 'name': 'Wise Owl School Age Care', 'address': '3525 13th Avenue, Regina, SK, S4T 1Z5', 'phone': '306-522-5291', 'lat': 50.4447892, 'lng': -104.6318807}, {'type': 'Group family child care home', 'name': 'Gemma Lopez', 'address': '1247 Retallack Street, Regina, SK, S4T 2H7', 'phone': '306-450-3605', 'lat': 50.4588626, 'lng': -104.6221789}, {'type': 'Centre, Accepts infants 6 weeks - 18 months, Extended hours', 'name': 'Stepping Stones, Elphinstone', 'address': '1561 Elphinstone Street, Regina, SK, S4T 3M9 (North Central)', 'phone': '306-352-2533', 'lat': 50.4539713, 'lng': -104.6306993}, {'type': 'Centre, Accepts infants 6 weeks - 18 months, Teen parent infant centre', 'name': 'Scott Infant and Toddler Centre', 'address': '3355 6th Avenue, Regina, SK, S4T 4L8', 'phone': '306-525-2344', 'lat': 50.4594051, 'lng': -104.6307978}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'Prairie Lily Early Learning Centre - Sacred Heart', 'address': '1325 Argyle Street, Regina, SK, S4T 2Z8', 'phone': '306-949-0090', 'lat': 50.4575594, 'lng': -104.631677}, {'type': 'Home', 'name': 'Belinda Wrobel', 'address': '2735 Winnipeg Street, Regina, SK, S4P 1J1 (Arnheim Place)', 'phone': '306-525-6632', 'lat': 50.4355579, 'lng': -104.5948595}, {'type': 'Centre', 'name': 'Turtle Park Co-operative Day Care Centre', 'address': '3100 – 20th Avenue, Regina, SK, S4S 0N8 (Normandy Heights)', 'phone': '306-584-9344', 'lat': 50.4329689, 'lng': -104.6262201}, {'type': 'Home', 'name': 'Jodi Anderson', 'address': '2600 Coronation Street, Regina, SK, S4S 0L3 (River Heights)', 'phone': '306-352-2892', 'lat': 50.4375831, 'lng': -104.6365737}, {'type': 'Group family child care home', 'name': 'Emily Camposano', 'address': '2100 Pasqua Street, Regina, SK, S4T 4M2', 'phone': '306-241-6333', 'lat': 50.4453367, 'lng': -104.6412506}, {'type': 'Group family child care home', 'name': 'Shazia Qasim', 'address': '2101 Edward Street, Regina, SK, S4T 4N5', 'phone': '306-520-8722', 'lat': 50.44536069999999, 'lng': -104.6420081}, {'type': 'Home', 'name': 'Abida Sultana', 'address': '3635 Normandy Avenue, Regina, SK, S4S 0X8', 'phone': '306-209-9200', 'lat': 50.4337114, 'lng': -104.6337339}, {'type': 'Centre', 'name': 'Seven Stones Child Care', 'address': '1101 Princess Street, Regina, SK, S4T 1G8', 'phone': '306-525-3960', 'lat': 50.46075159999999, 'lng': -104.6349381}, {'type': 'Home', 'name': 'Meherun Nesha', 'address': '715 Robinson Street, Regina, SK, S4T 2M2', 'phone': '306-757-9867', 'lat': 50.4673868, 'lng': -104.6236676}, {'type': 'Centre', 'name': 'Child Care Centre Co-operative', 'address': '105 College Avenue East, Regina, SK, S4N 0V5, (Arnheim Place)', 'phone': '306-757-2919', 'lat': 50.4406556, 'lng': -104.5810639}, {'type': 'Accepts infants 6 weeks - 18 months, Centre', 'name': 'Circle Project Infant Centre', 'address': '4401 Dewdney Avenue, Regina, SK, S4T 1B3 (Coventry Place)', 'phone': '306-949-4911', 'lat': 50.4549186, 'lng': -104.6440962}, {'type': 'Home, Group family child care home', 'name': 'Shaista Shaheen', 'address': '670 Garnet Street, Regina, SK, S4T 2W8', 'phone': '306-584-9469', 'lat': 50.4683004, 'lng': -104.6272326}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'Stepping Stones – Broad', 'address': '545 Broad Street, Regina, SK, S4R 1X5 (Highland Park)', 'phone': '306-791-3315', 'lat': 50.4702451, 'lng': -104.6061001}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': "Circle Project Children's Centre", 'address': '1115 Pasqua Street, Regina, SK, S4T 4L1', 'phone': '306-569-3988', 'lat': 50.46126599999999, 'lng': -104.6407431}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'Regina Eastview Day Care', 'address': '128 – 6th Avenue East, Regina, SK, S4N 5A5 (Eastview)', 'phone': '306-525-5543', 'lat': 50.4600158, 'lng': -104.582554}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'Orr Centre Daycare Inc.', 'address': '358 Century Crescent, Regina, SK, S4T 6M1', 'phone': '306-559-1001', 'lat': 50.4535905, 'lng': -104.6478239}, {'type': 'Centre', 'name': 'Sandcastles Coventry Road', 'address': '9 Coventry Road, Regina, SK, S4T 5Z4', 'phone': '306-545-9001', 'lat': 50.458945, 'lng': -104.6445283}, {'type': 'Home', 'name': 'Dianne Barnes', 'address': '713 Argyle Street, Regina, SK, S4T 3P7 (North Central)', 'phone': '306-352-1575', 'lat': 50.4674059, 'lng': -104.632289}, {'type': 'Group family child care home', 'name': 'Ambreen Majeed', 'address': '475 Ottawa Street, Regina, SK, S4R 1N8', 'phone': '306-352-0994', 'lat': 50.4710049, 'lng': -104.6003022}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'Adult Campus Child Care Centre', 'address': '4210 4th Avenue, Regina, SK, S4T 0H6', 'phone': '306-757-8140', 'lat': 50.46361169999999, 'lng': -104.6417587}, {'type': 'Accepts infants 6 weeks - 18 months', 'name': "YWCA Deanna's Den", 'address': '1855 2nd Avenue North, Regina, SK, S4R 0Y1', 'phone': '306-359-4425', 'lat': 50.47215749999999, 'lng': -104.6075072}, {'type': 'Centre', 'name': "YWCA Sally's Place", 'address': '1855 2nd Avenue North, Regina, SK, S4R 0Y1', 'phone': '306-359-4425', 'lat': 50.47215749999999, 'lng': -104.6075072}, {'type': 'Home', 'name': 'Nazneen Kashif', 'address': '3207 Westgate Avenue, Regina, SK, S4S 1B4', 'phone': '306-450-6550', 'lat': 50.4252566, 'lng': -104.6264567}, {'type': 'Group family child care home, Home', 'name': 'Pamela Fuchs', 'address': '2775 Francis Street, Regina, SK, S4N 2R4 (Arnheim Place)', 'phone': '306-757-6056', 'lat': 50.4347448, 'lng': -104.5789875}, {'type': 'Centre', 'name': 'Bo-Peep Co-operative Day Care', 'address': '4834 Dewdney Avenue, Regina, SK, S4T 1B6 (Coventry Place)', 'phone': '306-545-3498', 'lat': 50.4555027, 'lng': -104.6507325}, {'type': 'Home, Group family child care home', 'name': 'Dawn Marie', 'address': '41 Calder Crescent, Regina, SK, S4S 4A5 (Hillsdale)', 'phone': '306-584-1397', 'lat': 50.4228461, 'lng': -104.6104248}, {'type': 'Home', 'name': 'Julie Geiger', 'address': '2815 Harvey Street, Regina, SK, S4N 2N7', 'phone': '306-924-5908', 'lat': 50.4335697, 'lng': -104.5775463}, {'type': 'Home', 'name': 'Brenda Vogt', 'address': '468 Froom Crescent, Regina, SK, S4N 1T6', 'phone': '306-352-8878', 'lat': 50.44329099999999, 'lng': -104.5710953}, {'type': 'Centre', 'name': 'Ehrlo Early Learning Centre Imperial', 'address': '200 Broad Street, Regina, SK, S4R 1W9 (Highland Park)', 'phone': '306-751-4502', 'lat': 50.4765549, 'lng': -104.6074051}, {'type': 'Accepts infants 6 weeks - 18 months', 'name': 'Sandcastles Kings Road', 'address': '3615 Kings Road, Regina, SK, S4S 6Y4', 'phone': '306-584-9660', 'lat': 50.4222978, 'lng': -104.6261732}, {'type': 'Centre', 'name': 'YMCA South Child Care Centre McVeety', 'address': '38 Turgeon Crescent, Regina, SK, S4S 3Z7 (Hillsdale)', 'phone': '306-584-8123', 'lat': 50.4204429, 'lng': -104.6052214}, {'type': 'Home', 'name': 'Rizwana Shahid', 'address': '175 Scarth Street, Regina, SK, S4R 2B8', 'phone': '639-571-3435', 'lat': 50.4756884, 'lng': -104.6104609}, {'type': 'Centre', 'name': 'Gator Park Child Care Centre', 'address': '2941 Lakeview Avenue, Regina, SK, S4S 1G8 (South Lakeview)', 'phone': '306-584-2999', 'lat': 50.4212353, 'lng': -104.6260815}, {'type': 'Francophone, Accepts infants 6 weeks - 18 months', 'name': "Centre éducatif à la petite enfance de l'École du Parc", 'address': '621 Douglas Avenue East, Regina, SK, S4N 1H7', 'phone': '306-533-2432', 'lat': 50.4330152, 'lng': -104.5765748}, {'type': 'Home', 'name': 'Ayesha Tariq', 'address': '2305 Greer Court, Regina, SK, S4N 1T7', 'phone': '306-216-2204', 'lat': 50.4444668, 'lng': -104.5687955}, {'type': 'Home', 'name': 'Valerie Pretty', 'address': '159 Halifax Street, Regina, SK, S4R 1S7 (Cityview/Churchill Downs)', 'phone': '306-205-1559', 'lat': 50.4759146, 'lng': -104.6032051}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'Kids First Day Care Centre (Registered High School Students only)', 'address': '1069 – 14th Avenue East, Regina, SK, S4N 0T8 (Greer Court Area)', 'phone': '306-523-3318', 'lat': 50.4432555, 'lng': -104.5683709}, {'type': 'Centre', 'name': "Hope's Home John Paul II", 'address': '2200 25th Avenue, Regina, SK, S4S 4E6', 'phone': '306-205-8412', 'lat': 50.4192176, 'lng': -104.6129218}, {'type': 'Accepts infants 6 weeks - Kindergarten', 'name': 'Saplings Early Learning Child Care Centre - Hamilton', 'address': '125 Hamilton Street, Regina, SK, S4R 2A3', 'phone': '306-206-0267', 'lat': 50.4766159, 'lng': -104.6083315}, {'type': 'Centre', 'name': 'Bright Beginnings Early Childhood Centre', 'address': '3775 Regency Crescent, Regina, SK, S4R 8K5 (Regent Park)', 'phone': '306-543-7373', 'lat': 50.47273080000001, 'lng': -104.634967}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'God’s Little Blessings Child Care', 'address': '5130 – 4th Avenue, Regina, SK, S4T 0J7 (Rosemont)', 'phone': '306-543-1301', 'lat': 50.4631631, 'lng': -104.6550444}, {'type': 'Group family child care home', 'name': 'Saima Waheed', 'address': '1349 Forget Street, Regina, SK, S4T 4X2', 'phone': '306-501-7186', 'lat': 50.4574228, 'lng': -104.6492957}, {'type': 'Centre', 'name': 'Solid Futures Learning Centre Co-operative', 'address': '4705 – 1st Avenue, Regina, SK, S4T 7W4 (Rosemont)', 'phone': '306-543-7874', 'lat': 50.4670865, 'lng': -104.6486396}, {'type': 'Francophone, Accepts infants 6 weeks - 18 months', 'name': "La maison educative Gard'Amis", 'address': '2 Turgeon Crescent, Regina, SK, S4S 3Z6', 'phone': '306-525-9449', 'lat': 50.41859119999999, 'lng': -104.6051191}, {'type': 'Home', 'name': 'Sheila Pretty', 'address': '1546 Rupert Street, Regina, SK, S4N 1W2 (Glen Elm Park)', 'phone': '306-757-0111', 'lat': 50.45428159999999, 'lng': -104.5667022}, {'type': 'Home', 'name': 'Lubna Aamir', 'address': '468 Edward Street, Regina, SK, S4R 4W4', 'phone': '306-550-4577', 'lat': 50.47123209999999, 'lng': -104.6427355}, {'type': 'Centre', 'name': 'YMCA Albert Street Childcare Centre', 'address': '3801 Albert Street, Regina, SK, S4S 3R4', 'phone': '306-757-9622', 'lat': 50.4185068, 'lng': -104.61689}, {'type': 'Group family child care home, Extended hours', 'name': 'Maria Cecilia Melanson', 'address': '3048 25th Avenue, Regina, SK, S4S 1K9', 'phone': '306-541-3548', 'lat': 50.4189593, 'lng': -104.6252588}, {'type': 'Centre, Francophone', 'name': "Centre Educatif Gard'Amis", 'address': '1601 Cowan Crescent, Regina, SK, S4S 4C4 (Hillsdale)', 'phone': '306-525-9448', 'lat': 50.4179453, 'lng': -104.6029876}, {'type': 'Home, Group family child care home, 24 hours', 'name': 'Farzana Siddiqui', 'address': '1433 Uhrich Avenue, Regina, SK, S4S 3P7', 'phone': '306-585-1966', 'lat': 50.41251159999999, 'lng': -104.6028514}, {'type': 'Home', 'name': 'Kaylee Stevenson', 'address': '3516 King Street, Regina, SK, S4S 1G7', 'phone': '306-717-6797', 'lat': 50.4219696, 'lng': -104.638473}, {'type': 'Home', 'name': 'Sharlene Nomura', 'address': '1541 Regent Street, Regina, SK, S4N 1S1 (Glen Elm Park)', 'phone': '306-757-8251', 'lat': 50.4543705, 'lng': -104.5647}, {'type': 'Centre', 'name': 'Montessori School of Regina, Inc. (South Location)', 'address': '3515 Pasqua Street, Regina, SK, S4S 7G9', 'phone': '306-522-1500', 'lat': 50.4234382, 'lng': -104.6403741}, {'type': 'Group family child care home', 'name': 'Saima Babir', 'address': '2 Sheppard Street, Regina, SK, S4R 3M6', 'phone': '306-580-6303', 'lat': 50.47951219999999, 'lng': -104.6238273}, {'type': 'Home', 'name': 'Dai Vu', 'address': '1628 Oxford Street, Regina, SK, S4N 4M2', 'phone': '306-999-1992', 'lat': 50.4528987, 'lng': -104.5609478}, {'type': 'Home, 24 hours', 'name': 'Toni-Lynn Vanin', 'address': '1352 Grosvenor Street, Regina, SK, S4N 1R1 (Glencairn)', 'phone': '306-737-1063', 'lat': 50.4571315, 'lng': -104.5624413}, {'type': 'Centre', 'name': 'pamināwasowin', 'address': '1 First Nations Way, Regina, SK, S4S 7K2', 'phone': '306-790-5950,', 'lat': 50.4191999, 'lng': -104.58083}, {'type': 'Centre', 'name': 'Awasis Childcare Co-operative', 'address': '3737 Wascana Parkway, Regina, SK, S4S 0A2 (South, Near University)', 'phone': '306-585-5322', 'lat': 50.4187823, 'lng': -104.5920929}, {'type': 'Centre', 'name': 'Wascana Day Care Co-operative', 'address': '3737 Wascana Parkway, Regina, SK, S4S 0A2 (South, Near University)', 'phone': '306-585-5311', 'lat': 50.4187823, 'lng': -104.5920929}, {'type': 'Group family child care home', 'name': 'Shazia Tahir', 'address': '94 Munroe Place, Regina, SK, S4S 4P7', 'phone': '306-807-1904', 'lat': 50.4144766, 'lng': -104.6010983}, {'type': 'Home, Extended hours', 'name': 'Lorna Kelln', 'address': '17 Halleran Crescent, Regina, SK, S4R 3Z3 (Coronation Park)', 'phone': '306-525-3381', 'lat': 50.4795555, 'lng': -104.6336932}, {'type': 'Group family child care home', 'name': 'Farzana Naznin', 'address': '94 McMurchy Avenue, Regina, SK, S4R 3G6', 'phone': '306-205-8723', 'lat': 50.482319, 'lng': -104.6259578}, {'type': 'Centre', 'name': 'Ducky Day Care Centre Co-operative', 'address': '97 McMurchy Avenue, Regina, SK, S4R 3G5 (Coronation Park)', 'phone': '306-543-1765', 'lat': 50.4817988, 'lng': -104.6260857}, {'type': 'Home', 'name': 'Chris Isaac', 'address': '5315 McKinley Avenue, Regina, SK, S4T 7M2 (Rosemont/Coventry Place)', 'phone': '306-924-2074', 'lat': 50.4685883, 'lng': -104.6566836}, {'type': 'Centre', 'name': 'Ehrlo Early Learning Centre, Gladys McDonald', 'address': '335 Garnet Street North, Regina, SK, S4R 3S8 (Coronation Park)', 'phone': '306-751-4500', 'lat': 50.48131309999999, 'lng': -104.6263353}, {'type': 'Centre', 'name': 'Glencairn Child Care Co-op', 'address': '88B Cavendish Street, Regina, SK, S4N 5G7 (Glencairn)', 'phone': '306-789-9677', 'lat': 50.4538296, 'lng': -104.5582778}, {'type': 'Home, Group family child care home', 'name': 'Michel Graham', 'address': '1223 8th Avenue North, Regina, SK, S4R 0E8', 'phone': '306-533-8237', 'lat': 50.4833593, 'lng': -104.598754}, {'type': 'Home, Group family child care home', 'name': 'Denise Bailas', 'address': '1106 – 8th Avenue North, Regina, SK, S4R 8M8 (Cityview/Churchill Downs)', 'phone': '306-545-0790', 'lat': 50.478874, 'lng': -104.606515}, {'type': 'Centre', 'name': 'Montessori School of Regina, Inc. (East Location)', 'address': '101 Mayfield Road, Regina, SK, S4V 0B5', 'phone': '306-751-0093', 'lat': 50.4295821, 'lng': -104.5624122}, {'type': 'Home', 'name': 'Uzma Saifullah', 'address': '4300 Acadia Drive, Regina, SK, S4S 4C5', 'phone': '306-580-0850', 'lat': 50.41163479999999, 'lng': -104.6036535}, {'type': 'Centre', 'name': 'YMCA South Child Care Centre Massey', 'address': '131 Massey Road, Regina, SK, S4S 4N3 (Hillsdale)', 'phone': '306-584-8823', 'lat': 50.41138189999999, 'lng': -104.6083253}, {'type': 'Home', 'name': 'Beverly Wason', 'address': '46 Stapleford Crescent, Regina, SK, S4R 4S5 (Regent Park)', 'phone': '306-569-0445', 'lat': 50.4787058, 'lng': -104.6474347}, {'type': 'Home, Group family child care home', 'name': 'Nataliya Fedechko', 'address': '74 Sommerfeld Drive, Regina, SK, S4V 0C5 (University Park)', 'phone': '306-552-8550', 'lat': 50.4275042, 'lng': -104.5630247}, {'type': 'Home', 'name': 'Kayla Nelson', 'address': '4231 Castle Road, Regina, SK, S4S 4N4', 'phone': '306-550-3233', 'lat': 50.410801, 'lng': -104.6001824}, {'type': 'Centre', 'name': 'Ehrlo Early Learning Centre, Wilfrid Walker', 'address': '2102 Wagman Drive East, Regina, SK, S4V 0R1 (Gardiner Park)', 'phone': '306-751-4506', 'lat': 50.4402521, 'lng': -104.5530598}, {'type': 'Centre', 'name': 'Gardiner Park Child Care Association', 'address': '380 Gardiner Park Court, Regina, SK, S4V 1R9 (Gardiner Park)', 'phone': '306-789-7333', 'lat': 50.4355777, 'lng': -104.5546201}, {'type': 'Home, Extended hours', 'name': 'Cindy Emery', 'address': '2206 Dewdney Avenue East, Regina, SK, S4N 4C9 (Glencairn)', 'phone': '306-789-9175', 'lat': 50.4553004, 'lng': -104.552295}, {'type': 'Group family child care home', 'name': 'Elfie Nkongolo', 'address': '4127 Pasqua Street, Regina, SK, S4S 6H3', 'phone': '306-559-4094', 'lat': 50.4129468, 'lng': -104.640636}, {'type': 'Group family child care home', 'name': 'Sabrina Sabourin', 'address': '2211 Wagman Drive East, Regina, SK, S4V 0P7', 'phone': '306-737-7032', 'lat': 50.4383916, 'lng': -104.5517692}, {'type': 'Group family child care home', 'name': 'Purti Soni', 'address': '23 Sunset Drive, Regina, SK, S4S 2R4', 'phone': '306-550-1338', 'lat': 50.4085756, 'lng': -104.622632}, {'type': 'Group family child care home', 'name': 'Frehiwet Asfaha', 'address': '2220 7th Avenue East, Regina, SK, S4N 4S9', 'phone': '306-219-2119', 'lat': 50.458521, 'lng': -104.5516841}, {'type': 'Group family child care home', 'name': 'Laxmi Ramanathan', 'address': '69 Krauss Street, Regina, SK, S4T 6G5', 'phone': '306-515-2310', 'lat': 50.46389199999999, 'lng': -104.6708516}, {'type': 'Home, Group family child care home', 'name': 'Nazia Mir', 'address': '115 Scrivener Crescent, Regina, SK, S4N 4V6', 'phone': '306-205-1070', 'lat': 50.4591977, 'lng': -104.551229}, {'type': 'Group family child care home', 'name': 'Bilal Syed', 'address': '8 Dolphin Bay, Regina, SK, S4S 2L9', 'phone': '306-737-7756', 'lat': 50.4073997, 'lng': -104.6093057}, {'type': 'Home', 'name': 'Melanie Martin', 'address': '126 Salemka Crescent, Regina, SK, S4R 7S1 (Argyle Park)', 'phone': '306-546-2554', 'lat': 50.4875475, 'lng': -104.6312433}, {'type': 'Home', 'name': 'Rafiqun Nisa', 'address': '4663 Curtiss Avenue, Regina, SK, S4W 0A4', 'phone': '306-205-4869', 'lat': 50.4134174, 'lng': -104.6479735}, {'type': 'Home', 'name': 'Jahanzeb Naz Jamil', 'address': '4667 Curtiss Avenue, Regina, SK, S4W 0A4', 'phone': '306-999-1999', 'lat': 50.4134737, 'lng': -104.6481777}, {'type': 'Group family child care home', 'name': 'Maurvi Bhatt', 'address': '4812 Wright Road, Regina, SK, S4W 0A7', 'phone': '306-351-3091', 'lat': 50.4136253, 'lng': -104.6508131}, {'type': 'Home', 'name': 'Samantha Irvine', 'address': '34 Hodges Crescent, Regina, SK, S4N 4R3', 'phone': '306-529-9396', 'lat': 50.45275849999999, 'lng': -104.5466376}, {'type': 'Home, Group family child care home', 'name': 'Majbeen Khawar', 'address': '4820 Wright Road, Regina, SK, S4W 0A7', 'phone': '639-571-4489', 'lat': 50.4134637, 'lng': -104.6511292}, {'type': 'Home', 'name': 'Lee Ann Tymo', 'address': '7 Woodsworth Crescent, Regina, SK, S4T 7A9', 'phone': '306-535-7585', 'lat': 50.4738189, 'lng': -104.6662511}, {'type': 'Francophone, Group family child care home', 'name': 'Geraldine Natacha Ramsamy-Louise', 'address': '5081 Snowbirds Crescent, Regina, SK, S4W 0H5', 'phone': '306-501-7080', 'lat': 50.4143171, 'lng': -104.6541431}, {'type': 'Centre', 'name': 'Harbour Landing Village Child Care Centre', 'address': '4000 James Hill Road, Regina, SK, S4W 0N1', 'phone': '306-559-5545', 'lat': 50.4144436, 'lng': -104.6600514}, {'type': 'Accepts infants 6 weeks - 18 months', 'name': 'Umme Abiha', 'address': '2406 Crowe Street East, Regina, SK, S4V 0V7', 'phone': '306-201-7259', 'lat': 50.4345795, 'lng': -104.548605}, {'type': 'Extended hours, Home', 'name': 'Amanda McCall', 'address': '71 Sibbald Crescent, Regina, SK, S4T 7L6', 'phone': '306-531-7062', 'lat': 50.4661301, 'lng': -104.6750138}, {'type': 'Group family child care home', 'name': 'Cynthia Kalina', 'address': '99 Lockwood Road, Regina, SK, S4S 3G3', 'phone': '306-209-4489', 'lat': 50.4054085, 'lng': -104.6257726}, {'type': 'Group family child care home', 'name': 'Viktoriia Akulova', 'address': '150 Bentley Drive, Regina, SK, S4N 4S6', 'phone': '306-450-9012', 'lat': 50.4546488, 'lng': -104.5451668}, {'type': 'Group family child care home', 'name': 'Arpna Kumari', 'address': '903 Broad Street North, Regina, SK, S4R 5V6', 'phone': '306-550-5236', 'lat': 50.49147010000001, 'lng': -104.6059}, {'type': 'Home, Group family child care home, Francophone', 'name': 'Khady Bodian', 'address': '3328 Grant Road, Regina, SK, S4S 5H5 (Whitmore Park)', 'phone': '306-585-1929', 'lat': 50.4083964, 'lng': -104.5973565}, {'type': 'Group family child care home', 'name': 'Hardeep Lehal', 'address': '67 Bothwell Crescent, Regina, SK, S4R 5Y7', 'phone': '306-999-1799', 'lat': 50.49181919999999, 'lng': -104.599397}, {'type': 'Group family child care home', 'name': 'Sonamben Desai', 'address': '3712 Gordon Road, Regina, SK, S4S 5X2', 'phone': '306-560-0192', 'lat': 50.4057386, 'lng': -104.6344789}, {'type': 'Centre', 'name': 'Play & Discover Early Learning Centre Inc.', 'address': '4500 Wascana Parkway, Box 556, Regina, SK, S4P 3A3 (South, Near University)', 'phone': '306-775-7916', 'lat': 50.4079646, 'lng': -104.5812544}, {'type': 'Group family child care home', 'name': 'Musarrat Afza', 'address': '5110 Canuck Crescent, Regina, SK, S4W 0G4', 'phone': '306-206-0863', 'lat': 50.4166568, 'lng': -104.6536315}, {'type': 'Group family child care home', 'name': 'Sauvine Deugouelieu Ngueptchouang', 'address': '2926 Partridge Crescent, Regina, SK, S4R 8J5', 'phone': '306-450-6514', 'lat': 50.4924519, 'lng': -104.6238707}, {'type': 'Centre', 'name': 'Bright Beginnings Early Childhood Centre-Argyle', 'address': '280 Sangster Blvd., Regina, SK, S4R 7H5 (Argyle Park)', 'phone': '306-543-3220', 'lat': 50.4909963, 'lng': -104.63195}, {'type': 'Centre', 'name': 'Kidzone Child Care', 'address': '93 Lincoln Drive, Regina, SK, S4S 6P1 (Albert Park)', 'phone': '306-586-5505', 'lat': 50.40243299999999, 'lng': -104.6318816}, {'type': 'Centre', 'name': 'Prairie Lily Early Learning Centre, Ruth M. Buck', 'address': '6330 – 7th Avenue North, Regina, SK, S4T 7J1 (Normanview)', 'phone': '306-949-6684', 'lat': 50.4764026, 'lng': -104.6709693}, {'type': 'Group family child care home', 'name': 'Thi (Hien) Dinh', 'address': '1247 James Crescent, Regina, SK, S4N 6A4', 'phone': '306-999-1990', 'lat': 50.4601727, 'lng': -104.5425008}, {'type': 'Group family child care home', 'name': 'Jessie Knibbs', 'address': '137 Dalgliesh Drive, Regina, SK, S4R 5T1', 'phone': '306-531-2972', 'lat': 50.4855837, 'lng': -104.6549999}, {'type': 'Group family child care home', 'name': 'Nicole Funke', 'address': '179-A Wells Street, Regina, SK, S4R 5Z6', 'phone': '306-539-6197', 'lat': 50.4890665, 'lng': -104.6464096}, {'type': 'Group family child care home', 'name': 'Sarabjit Kaur', 'address': '2 Bannister Bay, Regina, SK, S4R 8A8', 'phone': '306-737-7083', 'lat': 50.487088, 'lng': -104.6529711}, {'type': 'Home', 'name': 'Jade Kampman', 'address': '2330 Hanover Crescent, Regina, SK, S4V 0Z6', 'phone': '306-551-1464', 'lat': 50.4242307, 'lng': -104.5496709}, {'type': 'Group family child care home', 'name': 'Iffat Tahira', 'address': '3007 Phaneuf Crescent, Regina, SK, S4V 1T6', 'phone': '306-737-3249', 'lat': 50.4400424, 'lng': -104.5399725}, {'type': 'Francophone, Group family child care home, Home', 'name': 'Anastasie Mbuyi-Tshiasuma', 'address': '95 Plainsview Drive, Regina, SK, S4S 6K1 (Albert Park)', 'phone': '306-586-8459', 'lat': 50.3996452, 'lng': -104.619388}, {'type': 'Centre', 'name': 'Whitmore Park Child Care Co-op', 'address': '15 Birchwood Road, Regina, SK, S4S 5N3 (Whitmore Park)', 'phone': '306-586-7532', 'lat': 50.40046299999999, 'lng': -104.6041389}, {'type': 'Home', 'name': 'Crystal Gordon', 'address': '5641 Cederholm Avenue, Regina, SK, S4W 0M9', 'phone': '306-515-1924', 'lat': 50.41308, 'lng': -104.66215}, {'type': 'Group family child care home', 'name': 'Saima Adeel', 'address': '1179 Ferguson Crescent, Regina, SK, S4N 6V6', 'phone': '613-709-5403', 'lat': 50.4602562, 'lng': -104.5409052}, {'type': 'Home', 'name': 'Anna Siudut', 'address': '6131 7th Avenue North, Regina, SK, S4T 6V9', 'phone': '306-351-1377', 'lat': 50.4787534, 'lng': -104.6692896}, {'type': 'Home', 'name': 'Jennifer Evanochko', 'address': '1155 Ferguson Crescent, Regina, SK, S4N 6V6', 'phone': '306-529-2646', 'lat': 50.4603674, 'lng': -104.5397689}, {'type': 'Home', 'name': 'Dianelis Mesa Tejera', 'address': '2343 Riverbend Crescent, Regina, SK, S4V 1G5', 'phone': '306-990-0550', 'lat': 50.4410706, 'lng': -104.5379895}, {'type': 'Centre', 'name': 'Ehrlo Early Learning Centre, Ruth Pawson', 'address': '40 Weekes Crescent, Regina, SK, S4R 6X7 (Uplands)', 'phone': '306-751-4504', 'lat': 50.4955229, 'lng': -104.6049456}, {'type': 'Centre', 'name': 'Prairie Lily Early Learning Centre, Normanview', 'address': '78 Dempsey Avenue, Regina, SK, S4T 7M1 (Normanview)', 'phone': '306-949-6684', 'lat': 50.4761602, 'lng': -104.6737283}, {'type': 'Group family child care home', 'name': 'Nadia Tahir', 'address': '3106 Dewdney Avenue East, Regina, SK, S4N 5E4', 'phone': '306-580-8311', 'lat': 50.4553397, 'lng': -104.5383841}, {'type': 'Group family child care home', 'name': 'Aqeel Siddiqui', 'address': '146 Fuhrmann Crescent, Regina, SK, S4R 7Z3', 'phone': '306-206-0744', 'lat': 50.4862841, 'lng': -104.6580874}, {'type': 'Centre', 'name': 'Ehrlo Early Learning Centre, W.F. Ready', 'address': '2710 Helmsing Street, Regina, SK, S4V 0W9 (Wood Meadows)', 'phone': '306-751-2722', 'lat': 50.43725060000001, 'lng': -104.5397759}, {'type': 'Group family child care home', 'name': 'Shumaila Saeed', 'address': '2601 Narcisse Drive, Regina, SK, S4X 0M8', 'phone': '647-648-5256', 'lat': 50.49520709999999, 'lng': -104.6208325}, {'type': '24 hours, Group family child care home', 'name': 'Shazia Mumtaz', 'address': '1114 Jurasin Street North, Regina, SK, S4X 0K1', 'phone': '306-775-1786', 'lat': 50.4954917, 'lng': -104.6271433}, {'type': 'Group family child care home', 'name': 'Archana Geethakumari', 'address': '8 French Crescent, Regina, SK, S4R 6N4', 'phone': '306-515-3876', 'lat': 50.4923035, 'lng': -104.6478948}, {'type': 'Home', 'name': 'Mariya Elias', 'address': '432 Dalgliesh Drive, Regina, SK, S4R 6M7', 'phone': '306-581-7938', 'lat': 50.4910209, 'lng': -104.6524881}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'YMCA Harbour Landing Child Care Centre', 'address': '4417 James Hill Road, Regina, SK, S4W 0R9', 'phone': '306-585-3160', 'lat': 50.40765469999999, 'lng': -104.6590769}, {'type': 'Home', 'name': 'Shannon Grumbly', 'address': '178 Rodenbush Drive, Regina, SK, S4R 7Y1', 'phone': '306-347-8231', 'lat': 50.4980724, 'lng': -104.6019885}, {'type': 'Home', 'name': 'Chelsea Gottfried', 'address': '3159 Zech Place, Regina, SK, S4V 1Z3', 'phone': '306-541-3190', 'lat': 50.428514, 'lng': -104.5398148}, {'type': 'Home', 'name': 'Seema Rani', 'address': '3162 Mazurak Crescent, Regina, SK, S4X 0N2', 'phone': '306-519-1159', 'lat': 50.498548, 'lng': -104.6263381}, {'type': 'Group family child care home', 'name': 'Natalya Tatchuk', 'address': '935 Dutkowski Crescent, Regina, SK, S4N 6X7', 'phone': '306-537-3883', 'lat': 50.463319, 'lng': -104.5360801}, {'type': 'Accepts infants 6 weeks - 18 months', 'name': 'Fatema Khirun Nesa', 'address': '3126 Mazurak Crescent, Regina, SK, S4X 0N2', 'phone': '306-450-4978', 'lat': 50.4986426, 'lng': -104.6252778}, {'type': 'Home', 'name': 'Syeda Mustafa', 'address': '5421 Gordon Road, Regina, SK, S4W 0K6', 'phone': '306-580-4940', 'lat': 50.4050539, 'lng': -104.6585434}, {'type': 'Home', 'name': 'Oleksii Akulov', 'address': '3011 Hayden Park Road, Regina, SK, S4V 2W9', 'phone': '306-450-8330', 'lat': 50.4321232, 'lng': -104.5345448}, {'type': 'Group family child care home', 'name': 'Samina Mansoor', 'address': '2455 Broderick Bay, Regina, SK, S4V 1K6', 'phone': '639-997-6490', 'lat': 50.4403264, 'lng': -104.5315353}, {'type': 'Group family child care home', 'name': 'Hina Nadeem', 'address': '4530 Delhaye Way, Regina, SK, S4W 0P4', 'phone': '306-737-1939', 'lat': 50.4062364, 'lng': -104.6634348}, {'type': 'Centre', 'name': 'Prairie Grown Early Learning Centre Inc', 'address': '3125 Woodham Drive, Regina, SK, S4V 2R5', 'phone': '306-775-5050', 'lat': 50.42843430000001, 'lng': -104.536802}, {'type': 'Group family child care home', 'name': 'Shabnam Rizwan', 'address': '314 Dalgliesh Drive, Regina, SK, S4R 7M7', 'phone': '306-205-3999', 'lat': 50.49098619999999, 'lng': -104.6600378}, {'type': 'Home, Group family child care home', 'name': 'Janyne Foster', 'address': '3611 Hammstrom Way East, Regina, SK, S4N 7N4 (Creekside)', 'phone': '306-550-1449', 'lat': 50.45897309999999, 'lng': -104.5314431}, {'type': 'Group family child care home', 'name': 'Ayesha Nadeem', 'address': '4650 Padwick Crescent, Regina, SK, S4W 0C5', 'phone': '306-546-2624', 'lat': 50.40003420000001, 'lng': -104.6481684}, {'type': 'Group family child care home', 'name': 'Bishnu Poudel', 'address': '5388 Aerial Crescent, Regina, SK, S4W 0C9', 'phone': '306-450-7236', 'lat': 50.4026975, 'lng': -104.6563223}, {'type': 'Group family child care home', 'name': 'Nicole LaRose', 'address': '1335 Chatwin Crescent, Regina, SK, S4N 7N8', 'phone': '306-789-9610', 'lat': 50.45708519999999, 'lng': -104.5282249}, {'type': 'Centre', 'name': 'Rink Avenue Daycare Co-operative', 'address': '587 Rink Avenue, Regina, SK, S4X 2G1 (McCarthy Park)', 'phone': '306-545-7055', 'lat': 50.4874793, 'lng': -104.675069}, {'type': 'Home', 'name': 'Memuna Aggrey', 'address': '3722 Cormorant Drive, Regina, SK, S4N 7S4 (Parkridge)', 'phone': '306-761-0989', 'lat': 50.4656968, 'lng': -104.5282749}, {'type': 'Home', 'name': 'Deanna Morin', 'address': '348 Prairie View Drive, Regina, SK, S4Y 0B2', 'phone': '306-545-9521', 'lat': 50.4740761, 'lng': -104.6910673}, {'type': 'Group family child care home', 'name': 'Mobina Zahid', 'address': '2406 Jameson Crescent, Regina, SK, S4V 1J7', 'phone': '306-949-9435', 'lat': 50.4391447, 'lng': -104.524691}, {'type': 'Group family child care home', 'name': 'Galina Horovitc', 'address': '6339 Leger Bay, Regina, SK, S4X 2K4', 'phone': '306-205-8462', 'lat': 50.4907999, 'lng': -104.6732109}, {'type': 'Home', 'name': 'Maricel Fabian', 'address': '5622 Beacon Place, Regina, SK, S4W 0J7', 'phone': '306-717-8851', 'lat': 50.3988834, 'lng': -104.6617794}, {'type': 'Accepts infants 6 weeks - 18 months', 'name': 'Dhivya Rajkumar', 'address': '5612 Gilbert Crescent, Regina, SK, S4W 0J4', 'phone': '306-201-8045', 'lat': 50.3979344, 'lng': -104.6609869}, {'type': 'Group family child care home', 'name': 'Xiuhua Zhou', 'address': '6146 Wascana Court, Regina, SK, S4V 3E7', 'phone': '306-596-9988', 'lat': 50.4149507, 'lng': -104.5331498}, {'type': 'Home, Group family child care home', 'name': 'Galina Tsozik', 'address': '1354 Hahn Crescent, Regina, SK, S4X 4L4', 'phone': '306-543-2303', 'lat': 50.5001335, 'lng': -104.6570051}, {'type': 'Centre, Accepts infants 6 weeks - 18 months', 'name': 'YMCA North West Child Care Centre', 'address': '5939 Rochdale Blvd., Regina, SK, S4X 2P9 (McCarthy Park)', 'phone': '306-757-9622', 'lat': 50.4948748, 'lng': -104.6678914}, {'type': 'Centre', 'name': 'YMCA Rochdale Child Care Centre', 'address': '5939 Rochdale Blvd., Regina, SK, S4X 2P9 (McCarthy Park)', 'phone': '306-757-9622', 'lat': 50.4948748, 'lng': -104.6678914}, {'type': 'Home', 'name': 'Sonia Fagan', 'address': '1014 Mawson Bay, Regina, SK, S4X 2P6', 'phone': '306-533-0413', 'lat': 50.4931315, 'lng': -104.6770877}, {'type': 'Home, Group family child care home, 24 hours', 'name': 'Cristina Cruz', 'address': '3347 Green Bank Road, Regina, SK, S4V 1P2 (Greens On Gardiner)', 'phone': '306-209-1738', 'lat': 50.4225832, 'lng': -104.5196618}, {'type': 'Home', 'name': 'Alia Imran', 'address': '3146 Green Bank Road, Regina, SK, S4V 3P8', 'phone': '306-510-3751', 'lat': 50.42650680000001, 'lng': -104.5239256}, {'type': 'Home', 'name': 'Rowena Betoro', 'address': '3142 Green Bank Road, Regina, SK, S4V 3P8', 'phone': '306-201-9843', 'lat': 50.4266365, 'lng': -104.523878}, {'type': 'Group family child care home', 'name': 'Milian Lamichhane', 'address': '7070 Wascana Cove Drive, Regina, SK, S4V 3E9', 'phone': '306-351-5515', 'lat': 50.4173333, 'lng': -104.5282311}, {'type': 'Group family child care home', 'name': 'Maria Rahim', 'address': '3259 Valley Green Way, Regina, SK, S4V 3R1', 'phone': '306-541-3176', 'lat': 50.4266727, 'lng': -104.5226215}, {'type': 'Home, Group family child care home', 'name': 'Shagufta Iftikhar', 'address': '3637 Green Cedar Court, Regina, SK, S4V 1M4', 'phone': '306-584-9810', 'lat': 50.4223764, 'lng': -104.5232317}, {'type': 'Home, Group family child care home', 'name': 'Galina Krumer', 'address': '1587 Lakeridge Drive, Regina, SK, S4X 4L6 (Lakeridge)', 'phone': '306-529-3390', 'lat': 50.5037973, 'lng': -104.6589476}, {'type': 'Home, Group family child care home', 'name': 'Krystal Langford', 'address': '6935 Farrell Bay, Regina, SK, S4X 3V4', 'phone': '639-915-0503', 'lat': 50.4962105, 'lng': -104.6801355}, {'type': 'Home, Group family child care home', 'name': 'Raldaline Barabar', 'address': '4241 E Green Olive Way, Regina, SK, S4V 1P9', 'phone': '306-519-4838', 'lat': 50.4187677, 'lng': -104.5202369}, {'type': 'Centre', 'name': 'First Years Learning Centre Inc. - Greens', 'address': '5133 E Green Brooks Way, Regina, SK, S4V 3M4', 'phone': '306-359-7170', 'lat': 50.4242387, 'lng': -104.5104437}, {'type': 'Home', 'name': 'Ravi Atwal', 'address': '3346 Chuka Boulevard, Regina, SK, S4V 3K7', 'phone': '306-450-2671', 'lat': 50.42525000000001, 'lng': -104.5128322}, {'type': 'Centre', 'name': 'Park Play Early Learning Centre', 'address': '7451 Mapleford Blvd., Regina, SK, S4Y 0C6', 'phone': '306-910-1414', 'lat': 50.5007875, 'lng': -104.6881835}, {'type': 'Group family child care home', 'name': 'Khola Sajjad Syeda', 'address': '5404 Green Apple Drive, Regina, SK, S4V 3M8', 'phone': '306-581-8586', 'lat': 50.4212785, 'lng': -104.505115}, {'type': 'Centre', 'name': "Hope's Home Rosewood", 'address': '7695 Mapleford Boulevard, Regina, SK, S4Y 0C6', 'phone': '306-522-1516', 'lat': 50.5007801, 'lng': -104.6910385}]
    for i in centres[5:]:
        try:
            full_addr = i['address'].split(',')
            postal_code_split = full_addr[3].split(' ')
            postal_code = postal_code_split[0] + postal_code_split[1]
            new_daycare = Daycare(name=i['name'],
                                  about=i['type'],
                                  phone_no=i['phone'],
                                  lat=i['lat'],
                                  lng=i['lng'],
                                  street=full_addr[0],
                                  city=full_addr[1],
                                  province=full_addr[2],
                                  postal_code=postal_code)
            db.session.add(new_daycare)
            db.session.commit()
        except:
            pass


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
