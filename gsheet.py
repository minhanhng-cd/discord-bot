import os
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = os.getenv('STUDENT_SCORING')
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)

service = build('sheets', 'v4', credentials = creds)

def get_scores():
    data = service.spreadsheets().values().get(
      spreadsheetId = SPREADSHEET_ID,
      range = 'Summary!D:G').execute()
    values = list(data['values'][1:])
    names = [x[0] for x in values]
    scores = [int(x[1]) for x in values]
    ranks = [x[2] for x in values]
    week = int(values[1][3])

    return (names, scores, ranks, week)

print(get_scores())