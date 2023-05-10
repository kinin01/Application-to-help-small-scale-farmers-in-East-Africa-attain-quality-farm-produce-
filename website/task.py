from datetime import datetime
import math
from data import planting_procedures

def get_procedure_details(procedure_id):
    for procedure in planting_procedures():
        if procedure['id'] == procedure_id:
            return procedure
    return None 

def get_week(start_date):
    today  = datetime.now()
    date_difference = today - start_date
# change to this during production
    # days = date_difference.days
    # if days < 7:
    #     return 1
    # else:
    #     return math.ceil(days/7)

# comment the below during production
    minutes = int(date_difference.seconds/60)
    if minutes < 5:
        return 1
    else:
        return math.ceil(minutes/5)

