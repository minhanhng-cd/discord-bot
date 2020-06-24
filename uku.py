#!/usr/bin/env python3
import os

import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

# ----COMMANDS----

# Command: Show available commands
def help(message):
    response = """Here are what Uku can do!
    - `help`: Show available commands
    - `config`: Show configuration settings (Only work in development server)
    - `links`: Display important class links
    - `cheers`: Give you a random cheer-up!
    """
    return response

# Command: Get content of .env file
def config(message):

    # Only work in development server
    if message.guild.name != "Uku & Lele's Servants":
        return

    with open('.env','r') as f:
        response = f.read()
    return response

# Command: Send important links
def links(message):
    response = """Here are some useful links! Meowww
    - Learning Portal: <http://learning.coderschool.vn/courses/ftmle_philippines/unit/1#!module>
    - Google Drive: <https://drive.google.com/drive/folders/1rRz0c0gwAAdkQIz7eRlJoMbbCeDADSTE>
    - Performance Dashboard: <https://datastudio.google.com/u/0/reporting/1EmxAbhqjUuG8JaXZ9w-UCWEioW2U-5sU/page/IkS6>
    - Q&A: <https://hackmd.io/Lf4aEx-nSYWfHGmlGafGig?both>
    """
    return response

# Command: Cheer up
def cheers(message):
    with open('cheers.txt','r') as f:
        cheers = [line for line in f]
    return random.choice(cheers)
# ----------------

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

# Reponse to message
@client.event
async def on_message(message):
    # Check if message is sent by user
    if message.author == client.user:
        return

    # Check if bot name is mentioned
    if 'Uku' in [u.name for u in message.mentions]:
        command = message.content.split()[-1]
        response = eval(command + '(message)')

        # Break if reponse is empty
        if not response:
            return

        await message.channel.send(response)

client.run(TOKEN)
