import discord
import random
from datetime import datetime 
from helpers import gsheet
import numpy as np
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

# Command: Show available commands
def help(message, channel):
    response = """Here are what Uku & Lele can do!
    - `cheers`: Give you a random cheer-up!
    - `clear`: Clear recent messages sent by Uku & Lele
    - `hello`/`hi`/`heya`/`helu`/`hey`/`here`: Check-in!
    - `config`: Show configuration settings (Only work in development server)
    - `help`: Show available commands
    - `links`: Display important class links
    - `missing`: Show missing students
    - `predict`: Predict a cat/dog image (Attach a cat/dog image to the message)
    """
    return {'content': response}

# Command: Get content of .env file
def config(message, channel):

    # Only work in development server
    if message.guild.name != "Uku & Lele's Servants":
        return

    with open('.env','r') as f:
        response = f.read()
    return {'content': response}

# Command: Send important links
def links(message, channel):

    try:
        embed = discord.Embed(title = "Here are some useful links!", color=0xd74742)
    
        data = gsheet.get_metadata()

        links = data[data['Channel'] == channel].iloc[:, 2:].replace('',np.nan).dropna(axis = 1).T.iloc[:,0].to_dict()

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

    # Get channel_id from metadata
    metadata = gsheet.get_metadata()
    
    spreadsheetId = metadata[metadata['Channel'] == channel]['ID'].values
 
    if len(spreadsheetId) == 0:
        print(f'Channel {channel} not found')
        return
    
    else:
        spreadsheetId = spreadsheetId[0]

    today = datetime.strftime(datetime.now().date(), '%Y-%m-%d')

    try:
        # Get list of users and their Disord account
        users = gsheet.get_users(spreadsheetId)
        user = users[message.author.name]
    except:
        return {'content': f'Student {message.author.name} not found!'}

    # Generate unique key
    key = today + user + 'Attendance'
    
    # Check if key already exists
    if key in gsheet.get_keys(spreadsheetId):
        return

    # Generate Attendance data row
    body = {'values': [[today, user, 1, 'Attendance']]}

    # Append data row to Student Scoring file
    gsheet.check_in(body, spreadsheetId)

    # Send welcome message
    welcome = ['Hi','Hello','Welcome to class','Glad to see you','Welcome','Meow','You look great today']

    return {'content': f'{random.choice(welcome)}, {user}!'}

# Command: Clear all messages sent by bot
def clear(message, channel):
    return 'clear'

# Command: Predict an cat/dog image
#def predict(message, channel):

 #   try:
  #      url = message.attachments[0].url
   #     r= requests.get(url)
    #    with open('../attachment.jpg', 'wb') as file:
     #       file.write(r.content)

     #   with open('../attachment.jpg', 'rb') as file:
      #      image = discord.File(file)

       # pred, prob = classify(model, '../attachment.jpg')

        #message = f'Hi **{message.author.name}**! We are **{round((prob[0][0] * 100), 2)}%** sure that this is a **{pred.upper()}**!'
    
    #except Exception as err:
     #   print(err)
    #return {'content':message, 'file':image}

# Command: Show missing students
def missing(message, channel):
    try:
        # Get channel_id from metadata
        metadata = gsheet.get_metadata()
        spreadsheetId = metadata[metadata['Channel'] == channel]['ID'].values

        if len(spreadsheetId) == 0:
            print(f'Channel {channel} not found')
            return
        else:
            spreadsheetId = spreadsheetId[0]

        # Get list of users and their Disord account
        users = gsheet.get_users(spreadsheetId)

        today = datetime.strftime(datetime.now().date(), '%Y-%m-%d')

        log = gsheet.get_keys(spreadsheetId)

        count = 0
        missing = []

        for user in users.values():
            key = today + user + 'Attendance'
            
            if key not in log:
                count += 1
                missing.append(user)

        if count == 0:
            message = "Everybody is here! Meoww"
        else:
            message = f"We are missing {count} student(s):\n"

            for s in missing:
                message += f"- {s}\n"

    except Exception as err:
        print(err)

    return {'content': message}
