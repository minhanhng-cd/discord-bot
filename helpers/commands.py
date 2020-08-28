import discord
import random
from datetime import datetime 
from dotenv import load_dotenv
from helpers import gsheet
import numpy as np
<<<<<<< HEAD
import os
import requests

load_dotenv()
STUDENT_SCORING = os.getenv('STUDENT_SCORING')
BOT_NAME = os.getenv('BOT_NAME')
=======
#import tensorflow as tf
import requests

# model = tf.keras.models.load_model('models/catdog.h5')

# Preprocess an image
#def preprocess_image(image):
 #   image = tf.image.decode_jpeg(image, channels=3)
  #  image = tf.image.resize(image, [224, 224])
   # image /= 255.0  # normalize to [0,1] range

    #return image

# Read the image from path and preprocess
#def load_and_preprocess_image(path):
 #   image = tf.io.read_file(path)
  #  return preprocess_image(image)

# Predict & classify image
#def classify(model, image_path):

 #   preprocessed_imgage = load_and_preprocess_image(image_path)
  #  preprocessed_imgage = tf.reshape(preprocessed_imgage, (1,224 ,224 ,3))

   # prob = model.predict(preprocessed_imgage)
    #label = "Cat" if prob >= 0.5 else "Dog"
    #classified_prob = prob if prob >= 0.5 else 1 - prob
    
   # return label, classified_prob
>>>>>>> 8de48cedf7d9a88f7c28d48d4e3141e38d45ecb1

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

    # Generate Attendance data row
    body = {'values': [[today, user, 1, 'Attendance']]}

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

