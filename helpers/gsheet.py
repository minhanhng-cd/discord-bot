from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import pandas as pd
import numpy as np

from dotenv import load_dotenv
import os

SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)

service = build('sheets', 'v4', credentials = creds)

def get_metadata():
    """
    Get cohorts metadata
    Return: Pandas DataFrame of Metadata
    """
    COHORT_METADATA = os.getenv('COHORT_METADATA')

    data = service.spreadsheets().values().get(
      spreadsheetId = COHORT_METADATA,
      range = 'metadata!A:M').execute()['values']
    for i, row in enumerate(data[1:]):
        data[1:][i] += [''] * (len(data[0]) - len(row))
    df_data = {}

    for i, name in enumerate(data[0]):
        df_data[name] = [row[i] for row in data[1:]]

    df = pd.DataFrame(df_data)
    return df

def get_users(spreadsheetId, cohort=None):
    """
    Get students and their Discord name
    Return: Discord Name - StudentId Dictionary
    """
    data = service.spreadsheets().values().get(
        spreadsheetId = spreadsheetId,
        range = 'Look_Up!A3:E').execute()['values']

    # Filter by cohort
    if cohort:
        return {i[3]: i[0] for i in data if (i[4] == 'Active') & (i[2] == cohort)}
    else:
        return {i[3]: i[0] for i in data if i[4] == 'Active'}

def get_keys(spreadsheetId):
    """
    Get students attendance unique keys
    Return: List of Keys
    """
    data = service.spreadsheets().values().get(
        spreadsheetId = spreadsheetId,
        range = 'Log!A:D').execute()['values']

    values = list(data[1:])

    keys = [x[0] + x[1] + x[3] for x in values]

    return keys

def get_activity(spreadsheetId):
    """
    Get list of scoring system activities
    Return: List of activities
    """
    data = service.spreadsheets().values().get(
        spreadsheetId = spreadsheetId,
        range = 'Look_Up!S:S').execute()['values']
    
    return [activity[0] for activity in data[1:]]
    

def add_point(body, spreadsheetId):
    """
    Check student attendance in Student Scoring
    """
    service.spreadsheets().values().append(
        spreadsheetId = spreadsheetId,
        range = 'Log!A:D', 
        valueInputOption='USER_ENTERED',
        body = body).execute()

    return