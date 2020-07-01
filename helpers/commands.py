import discord
import random
from datetime import datetime 
from helpers import gsheet
import numpy as np

# Command: Show available commands
def help(message, channel):
    response = """Here are what Uku can do!
    - `cheers`: Give you a random cheer-up!
    - `clear`: Clear recent messages sent by Uku & Lele
    - `hello`/`hi`/`heya`/`helu`/`hey`/`here`: Check-in!
    - `config`: Show configuration settings (Only work in development server)
    - `help`: Show available commands
    - `links`: Display important class links
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
    embed = discord.Embed(title = "Here are some useful links!", color=0xd74742)
    
    data = gsheet.get_metadata()

    links = data[data['Channel'] == channel].iloc[:, 2:].replace('',np.nan).dropna(axis = 1).T.iloc[:,0].to_dict()

    embed.set_image(url = 'https://i.imgur.com/ZmMo5ay.png')

    for name, value in links.items():
        embed.add_field(name = name, value = value, inline = False)

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

    # Get list of users and their Disord account
    users = gsheet.get_users(spreadsheetId)

    today = datetime.strftime(datetime.now().date(), '%Y-%m-%d')

    try:
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

def clear(message, channel):
    return 'clear'

