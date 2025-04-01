import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from router import navigate_to

# Google Sheets setup
def get_google_sheets_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client

# Title
st.title("View Saved Estimates")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Estimate"):
        navigate_to("estimate")
with col2:
    if st.button("How to Count Windows"):
        navigate_to("how_to_count_windows")

try:
    # Connect to Google Sheets
    client = get_google_sheets_client()
    spreadsheet_id = st.secrets["SPREADSHEET_ID"]
    st.write(f"DEBUG: Using Spreadsheet ID: {spreadsheet_id}")  # Debug message
    sheet = client.open_by_key(spreadsheet_id).sheet1

    # Get all records
    records = sheet.get_all_records()
    st.write(f"DEBUG: Found {len(records)} records in the sheet.")

    if not records:
        st.warning("No saved estimates found.")
    else:
        # Extract account names for the dropdown
        account_names = [record["Account Name"] for record in records]
        selected_account = st.selectbox("Select an estimate to view:", account_names)

        # Find the selected record
        selected_record = next(record for record in records if record["Account Name"] == selected_account)

        # Parse the inputs and results
        try:
            inputs = json.loads(selected_record["Inputs"])
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse inputs for {selected_account}. The data may be corrupted. Error: {str(e)}")
            inputs = {}

        try:
            results = json.loads(selected_record["Results"])
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse results for {selected_account}. The data may be corrupted. Error: {str(e)}")
            results = {}

        # Display the estimate details
        st.header(f"Estimate for {selected_account}")
        st.subheader("Timestamp")
        st.write(selected_record["Timestamp"])

        st.subheader("Inputs")
        for key, value in inputs.items():
            st.write(f"{key.replace('_', ' ')}: {value}")

        st.subheader("Results")
        if results:
            for key, value in results.items():
                if key != "total":
                    st.write(f"{key.replace('_', ' ')}: {value}")
            if "total" in results:
                st.write(f"**TOTAL: {results['total']}**")
        else:
            st.write("No pricing results available.")

except Exception as e:
    st.error(f"Failed to load saved estimates. Error: {str(e)}")
