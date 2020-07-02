import os
from datetime import datetime 
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import pandas as pd
import numpy as np

load_dotenv()

SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = os.getenv('COHORT_METADATA')
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)

service = build('sheets', 'v4', credentials = creds)

def get_users():
    data = service.spreadsheets().values().get(
      spreadsheetId = SPREADSHEET_ID,
      range = 'misc!A:B').execute()
    
    return data['values']

def get_keys():
    data = service.spreadsheets().values().get(
      spreadsheetId = SPREADSHEET_ID,
      range = 'Log!A:D').execute()
    values = list(data['values'][1:])

    keys = [x[0] + x[1] + x[3] for x in values]

    return keys

data = np.array(service.spreadsheets().values().get(
      spreadsheetId = SPREADSHEET_ID,
      range = 'metadata!A:M').execute()['values'])

print(pd.DataFrame(data[1:, :], columns = data[0,:]))

# print(pd.DataFrame(get_users(), columns = ['name','username']))
# print(datetime.strftime(datetime.now().date(), '%Y-%m-%d'))
# print(datetime.strptime(date[-1], '%Y-%m-%d').date())