import datetime
import pickle
from unittest.mock import MagicMock, Mock, mock_open, patch

import colorama
import google.auth
from google.oauth2.credentials import Credentials

import rooms

colorama.init()


def test_authenticate():
    # Create a mock credentials object
    mock_credentials = Mock(spec=Credentials)
    mock_credentials.valid = True

    # Patch google.auth to return the mock credentials object
    with patch.object(google.auth, "default", return_value=(mock_credentials, None)):
        # Patch InstalledAppFlow to return the mock credentials object
        mock_flow = Mock()
        mock_flow.run_local_server.return_value = mock_credentials
        with patch(
            "rooms.InstalledAppFlow.from_client_secrets_file",
            return_value=mock_flow,
        ):
            # Patch builtins to mock open() and pickle.load()
            with patch("builtins.open", mock_open()):
                with patch.object(pickle, "load", return_value=mock_credentials):
                    creds = rooms.authenticate()
                    assert isinstance(creds, Credentials)
                    assert creds.valid


def test_get_calendar_list():
    # Create a mock for the Google Calendar API service
    service = MagicMock()

    # Generate a mock calendar list response
    calendar_list_response = {
        "items": [
            {
                "id": "calendar1@resource.com",
                "summary": "Calendar 1",
                "timeZone": "America/New_York",
            },
            {
                "id": "calendar2@resource.com",
                "summary": "Calendar 2",
                "timeZone": "Europe/London",
            },
        ],
        "nextPageToken": None,
    }
    # Set the mock service's calendarList().list().execute() method to return the mock response
    service.calendarList().list().execute.return_value = calendar_list_response

    # Call the function
    calendar_list = rooms.get_calendar_list(service)

    # Check that the returned list contains two entries with the correct information
    assert len(calendar_list) == 2
    assert calendar_list[0]["id"] == "calendar1@resource.com"
    assert calendar_list[0]["summary"] == "Calendar 1"
    assert calendar_list[0]["timeZone"] == "America/New_York"
    assert calendar_list[1]["id"] == "calendar2@resource.com"
    assert calendar_list[1]["summary"] == "Calendar 2"
    assert calendar_list[1]["timeZone"] == "Europe/London"


def test_check_availability_free(capsys):
    # Create a mock for the Google Calendar API service
    service = MagicMock()
    # Create a mock calendar entry
    calendar_entry = {"id": "123", "summary": "Ostrava Office-3-Room1"}
    # Create a mock freebusy response indicating the calendar is free
    freebusy_response = {"calendars": {"123": {"busy": []}}}
    service.freebusy().query().execute.return_value = freebusy_response

    # Call the function
    rooms.check_availability(service, calendar_entry)

    # Check the output
    assert colorama.Fore.GREEN + "FREE" in capsys.readouterr().out


def test_check_availability_busy(capsys):
    # Create a mock for the Google Calendar API service
    service = MagicMock()
    # Create a mock calendar entry
    calendar_entry = {"id": "123", "summary": "Ostrava Office-3-Room1"}
    # Create a mock freebusy response indicating the calendar is busy
    busy_end_time = (
        datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    ).strftime("%H:%M")
    freebusy_response = {
        "calendars": {
            "123": {
                "busy": [
                    {
                        "start": datetime.datetime.utcnow().isoformat() + "Z",
                        "end": (
                            datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                        ).isoformat()
                        + "Z",
                    }
                ]
            }
        }
    }
    service.freebusy().query().execute.return_value = freebusy_response

    # Call the function
    rooms.check_availability(service, calendar_entry)

    # Check the output
    assert colorama.Fore.RED + "BUSY until: " + busy_end_time in capsys.readouterr().out
