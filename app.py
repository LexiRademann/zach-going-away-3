from flask import Flask, request, render_template, redirect
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")  # Allow all origins

# Load the credentials from the environment variable
credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
if credentials_json:
    credentials_info = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
else:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

# Replace 'your_sheet_id' with the ID of your Google Sheet
SPREADSHEET_ID = '1UFs5Irb-u9QaL6Ngoos6JTGUCkECglbdpwqnFs1Ejbc'
# Replace 'Sheet1' with the name of the sheet you want to write to
RANGE_NAME = 'Sheet1!A1'

service = build('sheets', 'v4', credentials=credentials)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    attendance = request.form['attendance']
    events = request.form.getlist('events')
    message = request.form['message']

    # Format the data for the Google Sheet
    events_string = ', '.join(events) if events else attendance
    values = [[name, email, events_string, message]]

    body = {
        'values': values
    }
    try:
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        return jsonify({"success": True, "message": "RSVP submitted successfully"}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)