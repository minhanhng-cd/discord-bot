#!/usr/bin/env python3
import os
import discord
from dotenv import load_dotenv
from helpers import gsheet 
from helpers.commands import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

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
    if 'Uku & Lele' in [u.name for u in message.mentions]:
        channel = message.channel.category.name
        command = message.content.split()[-1].lower()

        if command in ['hi','hello','heya','helu','hey','here']:
            command = 'hello'

        try:
            response = eval(command + '(message, channel)')
        except:
            response = None

        history = await message.channel.history(limit = 50).flatten()

        await message.delete()

        if response == 'clear':
            for m in history:
                if (m.author.name == 'Uku & Lele') or ('Uku & Lele' in [u.name for u in m.mentions]) or ('<@&727541182510399650>' in m.content) and ('order' not in m.content):
                    try:
                        await m.delete()
                    except:
                        pass
            return

        # Break if reponse is empty
        if not response:
            return

        await message.channel.send(**response)

client.run(TOKEN)