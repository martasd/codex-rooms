Meeting Room Availability Checker
---------------------------------

This Python 3 script checks the availability of meeting rooms in the Ostrava office using the Google Calendar API. It queries the availability of the meeting rooms and prints the results to the console.

### Prerequisites

The script requires a `credentials.json` file in the same directory, which can be obtained by following the instructions at [https://developers.google.com/calendar/quickstart/python](https://developers.google.com/calendar/quickstart/python).

### Dependencies

The following dependencies need to be installed before running the script:

*   `google-auth`
*   `google-auth-oauthlib`
*   `google-auth-httplib2`
*   `google-api-python-client`
*   `colorama`

### How to run

1.  Clone the repository to your local machine.
2.  Follow the instructions at [https://developers.google.com/calendar/quickstart/python](https://developers.google.com/calendar/quickstart/python) to obtain the `credentials.json` file.
3.  Install the dependencies listed above using pip.
4.  Run the script using `python script.py` in your terminal.

### How it works

The script first checks for existing user credentials in a `token.pickle` file. If the file does not exist or the credentials are invalid, the user is prompted to log in and authorize the script to access their Google Calendar. Next, the script uses the Google Calendar API to query the availability of the meeting rooms in the Ostrava office. For each meeting room, it prints the status of the room ("FREE" or "BUSY until <end time>") to the console. The script checks availability for the next 30 minutes. The script runs continuously until all meeting rooms have been checked for availability.

### Limitations

The script only checks for the availability of meeting rooms in the Ostrava office. If you wish to use the script to check availability for a different location, you will need to modify the code to use the appropriate calendar IDs. The script also only checks availability for the next 30 minutes.

### Authors

This script was created by [OpenAI](https://openai.com/).

### License

This project is licensed under the MIT License.
