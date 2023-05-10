from website import create_app
from flask_migrate import Migrate
from  website import db
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from website.models import User
from website.task import get_procedure_details,get_week
from website.alert import send_message

app = create_app()
app.app_context().push()

def scheduled_message():
    with app.app_context():
        users = User.query.all()
        for user in users:
            if user.is_scheduled:
                print("scheduling")
                week = get_week(user.startdate)
                procedure = get_procedure_details(int(user.crop_id))
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
    scheduler.add_job(func=scheduled_message, trigger="interval", minutes=5)#change to number of minutes in a week
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

start_schedule()
# handle the migrations
migrate = Migrate(app,db)

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

if __name__ == '__main__':
    app.run(debug=True)