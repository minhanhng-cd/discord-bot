# CoderSchool Discord Bot

Hi, My name is Uku! I am a full-time cat at Mina's home and part-time Discord Bot at CoderSchool!

Useful links: 
- [Quick Tutorial](https://realpython.com/how-to-make-a-discord-bot-python/)
- [Documentation](https://discordpy.readthedocs.io/en/latest/)

## 1. Setup

1. Clone this repo

2. Navigate to discord-bot folder
```
cd discord-bot
```

3. Create a virtual environment
```
conda create --name discord-bot
```

4. Activiate virtual environment
```
conda activate discord-bot
```

5. Install dependencies
```
pip install -r requirements.txt
```

6. Create a `.env` file
```
vim .env
```
Hit the key `I` then paste the DISCORD_TOKEN and DISCORD_GUILD. Then hit `Esc`, type `:wq` and hit `Enter`

7. Run the bot script
```
python uku.py
```

#### For Google Sheet API
1. Download the file `credentials.json` in Google Drive folder `Discord Bot` and save it to the project folder `discort-bot`
2. Make sure that the `.env` file contains STUDENT_SCORING.
3. Run the script
It should print out the name of students in our class, their score and rank. The gsheet file is in `Discord Bot` folder, called `Test Date - Student Scoring`.
```
python gsheet.py
```

## 2. Submit your work
You should make changes/add new features to the projects in a seperate branch
```
git checkout -b <branch-name>
```
E.g. 
```
git checkout -b tom
```

Once you finish your work,
1. Get the latest update from `origin/master` branch
```
git pull origin master
```
2. Stage all changes
```
git add .
```
3. Commit your changes
```
git commit -m <commit-message>
```
E.g.
```
git commit - m "Fix bugs"
```
4. Push your branch to origin
```
git push origin <branch-name>
```
E.g.
```  
git push origin tom
```
Note: Do not push directly to `origin/master`

5. Create a pull request
Go to this Github > Pull requests > New pull request

6. Ask me to merge your changes with `origin/master`
