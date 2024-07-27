from flask import Flask, request, render_template, redirect
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# Replace 'credentials.json' with the path to your service account JSON file
SERVICE_ACCOUNT_FILE = 'credentials.json'
# Replace 'your_sheet_id' with the ID of your Google Sheet
SPREADSHEET_ID = '1UFs5Irb-u9QaL6Ngoos6JTGUCkECglbdpwqnFs1Ejbc'
# Replace 'Sheet1' with the name of the sheet you want to write to
RANGE_NAME = 'Sheet1!A1'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

service = build('sheets', 'v4', credentials=credentials)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    values = [[name, email]]

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
        return render_template('success.html')  # Create a new template for success message
    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('error.html')  # Create a new template for error message

if __name__ == '__main__':
    app.run(debug=True)