from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from generic.utils import load_pickle
from generic.utils import print_warn

class Calender:
    def __init__(self, credentials_file_path, token_file_path = "", calender_scope = ['https://www.googleapis.com/auth/calendar']):
        self.creds = None
        self.token_file_path = token_file_path
        self.credentials_file_path = credentials_file_path
        self.calender_scope = calender_scope

    def set_credentials(self):
        self.creds = load_pickle(self.token_file_path)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file_path, self.calender_scope)
                self.creds = flow.run_local_server()

            # Save the credentials for the next run
            location = os.path.dirname(self.credentials_file_path)
            token_file_path = location + "/" + 'token.pickle'

            with open(token_file_path, 'wb') as token:
                pickle.dump(self.creds, token)

    def connect(self):
        self.set_credentials()
        service = build('calendar', 'v3', credentials=self.creds)
        return service
    
    def add_event(self, event):
        service = self.connect()
        try:
            event = service.events().insert(calendarId='primary', body=event).execute()
            print ('Event created: %s' % (event.get('htmlLink')))
        except:
            msg = str(event['summary']) + ": " + "event creation failed"
            print_warn(msg)
    
    def remove_event(self, eventId):
        service = self.connect()
        try:
            service.events().delete(calendarId='primary', eventId=eventId).execute()
        except:
            msg = "event" + " " + str(eventId) + " " + "not found"
            print_warn(msg)

if __name__ == "__main__":
    pass