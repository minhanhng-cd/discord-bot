from dotenv import load_dotenv
from helpers import gsheet
import os
import schedule
import time
from datetime import datetime

load_dotenv()
STUDENT_SCORING = os.getenv('STUDENT_SCORING')

def check_absence():
    today = datetime.strftime(datetime.now().date(), '%Y-%m-%d')

    # Get list of users and their Disord account
    users = gsheet.get_users(STUDENT_SCORING)

    # Get unique attendance key
    keys = [today + user + 'Attendance' for user in users.values()]

    body = {'values': []}

    # Deduct points of absence students
    for i, key in enumerate(keys):
        if key not in gsheet.get_keys(STUDENT_SCORING):
            body['values'].append([today, list(users.values())[i], -5, 'Attendance'])
   
    gsheet.add_point(body, STUDENT_SCORING)
    
    return

# Check absense every day at 18:00
schedule.every().monday.at("22:10").do(check_absence)
schedule.every().tuesday.at("22:10").do(check_absence)
schedule.every().wednesday.at("22:10").do(check_absence)
schedule.every().thursday.at("22:10").do(check_absence)
schedule.every().friday.at("22:10").do(check_absence)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute