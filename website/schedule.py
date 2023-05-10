import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from .models import User
from .task import get_procedure_details,get_week
from .alert import send_message

def scheduled_message():
    print("scheduling")
    users = User.query.all()
    for user in users:
        week = get_week(user.registerdate)
        crop_id = 1
        procedure = get_procedure_details(int(crop_id))
        for item in procedure['weeks']:
            if item['week'] == week:
                message = ""
                for activity in item['activities']:
                    message += activity
                try:
                    message = send_message(message=message,phone_number= f"+{user.phonenumber}")
                except:
                    pass

def start_schedule():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=scheduled_message, trigger="interval", minutes=5) #change to number of minutes in one one week
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())