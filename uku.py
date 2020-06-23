# bot.py
import os

import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

# ----COMMANDS----

# Command: Send important links
def important_links():
    response = """Here are some useful links! Meowww
    - Learning Portal: http://learning.coderschool.vn/courses/ftmle_philippines/unit/1#!module
    - Google Drive: https://drive.google.com/drive/folders/1rRz0c0gwAAdkQIz7eRlJoMbbCeDADSTE
    - Performance Dashboard: https://datastudio.google.com/u/0/reporting/1EmxAbhqjUuG8JaXZ9w-UCWEioW2U-5sU/page/IkS6
    """
    return response

# Command: Cheer up
def cheers():
    with open('cheers.txt','r') as f:
        cheers = [line for line in f]
    return random.choice(cheers)

commands = {'links': 'important_links()',
            'cheers': 'cheers()'}
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
        response = eval(commands[command])
        await message.channel.send(response)

client.run(TOKEN)