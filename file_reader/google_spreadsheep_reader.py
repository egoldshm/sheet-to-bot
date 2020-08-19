##################################################################
#                                                                #
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#               eitntt@gmail.com  - t.me/egoldshm                #
#    #      השימוש ללא אישור אסור לפי ההלכה ולפי הרישיון והחוק הבינלאומי
#                                                                #
##################################################################


from __future__ import print_function
import pickle
import os.path

from typing import List, Dict, Union, Any

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class google_spreadsheet_reader():
    def __init__(self, file_id, range_to_get):
        creds = None
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        path_of_token = os.path.join(THIS_FOLDER, 'token.pickle')
        if os.path.exists(path_of_token):
            with open(path_of_token, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                path_of_credentials = os.path.join(THIS_FOLDER, "credentials.json")
                flow = InstalledAppFlow.from_client_secrets_file(path_of_credentials, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=file_id,
                                    range=range_to_get).execute()
        self.values = result.get('values', [])

if __name__ == "__main__":
    x = google_spreadsheet_reader("1ypfEgxsDhthKTocTz0ZfuqRorV4ffd1vA4A1BfMxXwA","range")
    print(x.values)