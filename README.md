# CoderSchool Discord Bot

Hi, We are Uku & Lele! We are full-time cats at Mina's home and part-time Discord Bot at CoderSchool!

- `bot.py` provides commands and utilities for intructors and students to interact with the Scoring System from Discord.
- `missing.py` check missing students everyday at 18:00.

Useful links: 
- [Quick Tutorial](https://realpython.com/how-to-make-a-discord-bot-python/)
- [Documentation](https://discordpy.readthedocs.io/en/latest/)

## Tutorial

1. Clone this repo

2. Navigate to discord-bot folder
```
cd discord-bot
```

3. Create a virtual environment
```
pip install virtualenv
```
```
virtualenv discord-bot
```

4. Activiate virtual environment
```
source discord-bot/bin/activate
```

5. Install dependencies
```
pip install -r requirements.txt
```

6. Create a `.env` file
```
vim .env
```
Contents of `.env` file:
```
DISCORD_TOKEN={BOT DISCORD TOKEN}
DISCORD_GUILD={GUILD NAME}
COHORT_METADATA={METADATA SPREADSHEET ID}
BOT_NAME={BOT NAME}
STUDENT_SCORING={STUDENT SCORING SPREADSHEET ID}
```
7. Download Google Service Account credentials `credentials.json` and put in this folder.

8. Run the scripts
```
sh run
```