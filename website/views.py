# from curses import flash
from datetime import datetime
from flask import Blueprint, render_template, request, session,flash
from flask_login import login_required, current_user
from data import planting_procedures
from .models import Activity, Procedure, User, Weeks
from .task import get_procedure_details,get_week
from .alert import send_message
from twilio.rest import Client
import atexit
from . import db
views = Blueprint('views', __name__)

# home
@views.route('/')
def home():
    return  render_template('home.html', user=current_user)
# about
@views.route('/about')
def about():
    return render_template('about.html', user=current_user) 

PlantingProcedures= planting_procedures()

# planting procedures
@views.route('/crops' )
def crops():
    return render_template('crops.html', procedures =PlantingProcedures, user =current_user)

# Single procedure
@views.route('/crops/<int:id>')
def crop1(id):
    # procedure = get_procedure_details(id)
    procedure = Procedure.query.filter_by(id=id).first()
    return render_template('crop.html', procedure=procedure, user =current_user)

# Dashboard
@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views.route('/datatodatabase')
# @login_required
def datatodatabase():
    try:
        procedures = Procedure.query.all()
        if len(procedures) > 0:
            print(procedures)
            return f"<p>database already populated</p>"
        else:
            for item in planting_procedures():
                procedure = Procedure(
                    maintitle = item['maintitle'],
                    description = item['description']
                )
                db.session.add(procedure)
                db.session.commit()
                for w in item['weeks']:
                    week = Weeks(
                        title = w['title'],
                        procedure_id = procedure.id,
                    )
                    db.session.add(week)
                    db.session.commit()
                    print(w)
                    for a in w['activities']:
                        activity = Activity(
                            activity = a,
                            week_id = week.id
                        )
                        db.session.add(activity)
                        db.session.commit()
            return f"<p>database populated</p>"
    except Exception as err:
        raise(err)


# # Schedule
@views.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if request.method == 'GET':
        return render_template('procedures.html', procedures =PlantingProcedures,user=current_user)
    else:
        user_id = session["_user_id"]
        user = User.query.get(user_id)
        week = get_week(user.registerdate)
        id = request.form.get('procedure')
        # procedure = get_procedure_details(int(id))
        procedure = Procedure.query.filter_by(id=int(id)).first()
        for item in procedure.weeks:
            if item.id == week:
                message = ""
                for activity in item['activities']:
                    message += activity
                message = send_message(message=message,phone_number= f"+{user.phonenumber}")
                print(message.status)
        if user.is_scheduled == True:
            flash('Already Scheduled.', category='error')
        else:
            user.startdate = datetime.now()
            user.is_scheduled = True
            # changed here
            user.crop_id = int(id)
            db.session.commit()

            flash('Send succefully.', category='success')
        return render_template('procedures.html', user=current_user)

