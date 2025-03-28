import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="View Saved Estimates")

# Google Sheets setup
def get_google_sheets_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client

def load_estimates():
    try:
        client = get_google_sheets_client()
        spreadsheet_id = st.secrets["SPREADSHEET_ID"]
        sheet = client.open_by_key(spreadsheet_id).sheet1
        records = sheet.get_all_records()
        # DEBUG line below:
        st.write(f"DEBUG: Found {len(records)} records in the sheet.")
        return records
    except Exception as e:
        st.error(f"Failed to load estimates. Error: {str(e)}")
        return []

def delete_estimate(account_name):
    try:
        client = get_google_sheets_client()
        spreadsheet_id = st.secrets["SPREADSHEET_ID"]
        sheet = client.open_by_key(spreadsheet_id).sheet1
        all_records = sheet.get_all_records()
        row_to_delete = None
        for idx, record in enumerate(all_records, start=2):
            if record["Account Name"]
