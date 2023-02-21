"""
This script checks the availability of the meeting rooms in the Ostrava office.

It uses the Google Calendar API to query the availability of the meeting rooms
and prints the results to the console.

The script requires a credentials.json file in the same directory.

The credentials.json file can be obtained by following the instructions at
https://developers.google.com/calendar/quickstart/python
"""

from __future__ import print_function

import datetime
import os.path
import pickle

import colorama
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
]


colorama.init()


def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds


def get_calendar_list(service):
    page_token = None
    calendar_list = []
    while True:
        calendar_list_response = (
            service.calendarList().list(pageToken=page_token).execute()
        )
        for calendar_list_entry in calendar_list_response["items"]:
            if "resource" in calendar_list_entry["id"]:
                calendar_list.append(calendar_list_entry)
        page_token = calendar_list_response.get("nextPageToken")
        if not page_token:
            break
    return calendar_list


def check_availability(service, calendar_list_entry):
    print(
        colorama.Style.RESET_ALL
        + calendar_list_entry["summary"].replace("Ostrava Office-3-", ""),
        end=" is ",
    )
    free_busy_query = {
        "timeMin": datetime.datetime.utcnow().isoformat() + "Z",
        "timeMax": (
            datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        ).isoformat()
        + "Z",
        "timeZone": "Europe/London",
        "items": [{"id": calendar_list_entry["id"]}],
    }
    free_busy_response = service.freebusy().query(body=free_busy_query).execute()
    if free_busy_response["calendars"][calendar_list_entry["id"]]["busy"]:
        print(
            colorama.Fore.RED + "BUSY until:",
            free_busy_response["calendars"][calendar_list_entry["id"]]["busy"][0][
                "end"
            ][11:16],
        )
    else:
        print(colorama.Fore.GREEN + "FREE")


def main():
    creds = authenticate()
    service = build("calendar", "v3", credentials=creds)

    calendar_list = get_calendar_list(service)
    for calendar_list_entry in calendar_list:
        check_availability(service, calendar_list_entry)


if __name__ == "__main__":
    main()
