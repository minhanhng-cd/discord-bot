import discord
import random
from datetime import datetime 
from dotenv import load_dotenv
from helpers import gsheet
import numpy as np

import os
import requests

load_dotenv()
STUDENT_SCORING = os.getenv('STUDENT_SCORING')
BOT_NAME = os.getenv('BOT_NAME')

import requests

# Command: Show available commands
def help(message, channel):
    response = """Here are what Uku & Lele can do!
    - `cheers`: Give you a random cheer-up!
    - `clear`: Clear recent messages sent by Uku & Lele
    - `hello`/`hi`/`heya`/`helu`/`hey`/`here`: Check-in!
    - `give`: Give points to students (Instructors/TAs only). Format: `give {point} {activity} {notes (optional)} {mentions}`
    - `help`: Show available commands
    - `links`: Display important class links
    - `missing`: Show missing students
    """
    return {'content': response}

# Command: Send important links
def links(message, channel):

    try:
        embed = discord.Embed(title = "Here are some useful links!", color=0xd74742)
    
        data = gsheet.get_metadata()

        links = data[data['Channel'] == channel].iloc[:, 3:].replace('',np.nan).dropna(axis = 1).T.iloc[:,0].to_dict()

        embed.set_image(url = 'https://i.imgur.com/ZmMo5ay.png')

        for name, value in links.items():
            embed.add_field(name = name, value = value, inline = False)
    except Exception as err:
        print(err)
    return {'embed': embed}

# Command: Cheer up
def cheers(message, channel):
    with open('cheers.txt','r') as f:
        cheers = [line for line in f]
    return {'content':random.choice(cheers)}

# Command: Check-in
def hello(message, channel):

    # Check if it is weekend
    if datetime.now().weekday() in [5,6]:
        return {'content': f'There is no class today!'}

    today = datetime.strftime(datetime.now().date(), '%Y-%m-%d')

    try:
        # Get list of users and their Disord account
        users = gsheet.get_users(STUDENT_SCORING)

        if users == {}:
            return {'content': f'Cohort is inactive!'}

        user = users[message.author.name]
        
    except Exception as err:
        print(err)
        return {'content': f'Student {message.author.name} not found!'}

    # Generate unique key
    key = today + user + 'Attendance'
    
    # Check if key already exists
    if key in gsheet.get_keys(STUDENT_SCORING):
        return {'content': f'Student {message.author.name} has already checked-in today!'}

    now = datetime.now().time()

    late = datetime.strptime('10:15:00','%H:%M:%S').time()

    # Give point if on-time. minus point if late
    if  now > late:
        score = -2
    else:
        score = 1

    # Generate Attendance data row
    body = {'values': [[today, user, score, 'Attendance']]}

    # Append data row to Student Scoring file
    gsheet.add_point(body, STUDENT_SCORING)

    # Send welcome message
    welcome = ['Hi','Hello','Welcome to class','Glad to see you','Welcome','Meow','You look great today']

    return {'content': f'{random.choice(welcome)}, {message.author.name}!'}

# Command: Clear all messages sent by bot
def clear(message, channel):
    return 'clear'

# Command: Show missing students
def missing(message, channel):
    try:
        # Get channel_id from metadata
        metadata = gsheet.get_metadata()

        cohort = metadata[metadata['Channel'] == channel]['Cohort'].values[0]

        # Get list of users and their Disord account
        users = gsheet.get_users(STUDENT_SCORING, cohort)

        if users == {}:
            return {'content': f'Cohort is inactive!'}


        # Today
        today = datetime.strftime(datetime.now().date(), '%Y-%m-%d')

        # Unique keys from log
        log = gsheet.get_keys(STUDENT_SCORING)

        count = 0
        missing = []

        for discord_name, user in users.items():
            key = today + user + 'Attendance'
            
            if key not in log:
                count += 1
                missing.append(discord_name)

        if count == 0:
            message = "Everybody is here! Meoww"
        else:
            message = f"We are missing {count} student(s):\n"

            for s in missing:
                message += f"- {s}\n"

    except Exception as err:
        print(err)

    return {'content': message}

# Command: Give points to students
def give(message, channel):

    # Verify authorized users
    metadata = gsheet.get_metadata()

    authorized_users = metadata[metadata['Channel'] == channel]['Instructors'].values[0]
    
    if message.author.name not in authorized_users.split(','):
        return {'content': 'Authorization Error: Your are not allowed to give points!'}

    # Verify point
    point, activity = message.content.split()[2:4]

    try:
        assert int(point) > 0
    except:
        return {'content': 'Invalid Argument: Point must be integer larger than 0.'}

    # Verify activity
    valid_activities = gsheet.get_activity(STUDENT_SCORING)

    if activity not in valid_activities:
        return {'content': 'Invalid Argument: Activity not found.'}

    # List of mentioned students, excluding bot
    mentions = [u.name for u in message.mentions if u.name != BOT_NAME]
    # Verfiy users

    if len (mentions) == 0:
        return {'content': 'Invalid Argument: No student specified.'}

    try:
        users = gsheet.get_users(STUDENT_SCORING)

        if users == {}:
            return {'content': f'Cohort is inactive!'}

        students = []
        for s in mentions:
            students.append(users[s])
        
    except Exception as err:
        print(err)
        return {'content': f'Student {s} not found!'}

    # Notes
    notes = message.content.split()[4:]

    for i, word in enumerate(notes):
        # Exclude mentioned from notess
        if word.startswith('<@'):
            notes[i] = ''

    notes = ' '.join(notes)

    # Today
    today = datetime.strftime(datetime.now().date(), '%Y-%m-%d')

    # Generate data row
    body = {'values': [[today, student, point, activity, notes] for student in students]}

    # Append data row
    gsheet.add_point(body, STUDENT_SCORING)
    
    congrats = ['Good job', 'Great job', 'Spendid', 'You are amazing', 'Meoww', 'Keep it up']

    return {'content': f'{", ".join(mentions)} just earned **{point} point(s)** in **{activity}**! {random.choice(congrats)}!'}

