import streamlit as st
import json
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="CC Inc. Pricing Calculator")

# Google Sheets setup
def get_google_sheets_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client

def save_estimate(account_name, customer_info, inputs, results):
    try:
        client = get_google_sheets_client()
        spreadsheet_id = st.secrets["SPREADSHEET_ID"]
        st.write(f"Using Spreadsheet ID: {spreadsheet_id}")  # Debug message
        sheet = client.open_by_key(spreadsheet_id).sheet1

        # Check if the account name already exists
        all_records = sheet.get_all_records()
        row_to_update = None
        for idx, record in enumerate(all_records, start=2):  # Start at row 2 (after header)
            if record["Account Name"] == account_name:
                row_to_update = idx
                break

        # Prepare the data to save
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        customer_info_str = json.dumps(customer_info)
        inputs_str = json.dumps(inputs)
        results_str = json.dumps(results)

        # If the account name exists, update the existing row; otherwise, append a new row
        if row_to_update:
            sheet.update(f"A{row_to_update}:E{row_to_update}", [[account_name, timestamp, customer_info_str, inputs_str, results_str]])
        else:
            sheet.append_row([account_name, timestamp, customer_info_str, inputs_str, results_str])
        st.success(f"Estimate for {account_name} saved to Google Sheets!")
    except Exception as e:
        st.error(f"Failed to save estimate. Error: {str(e)}")
        raise e

# Initialize session state for inputs
if "inputs" not in st.session_state:
    st.session_state.inputs = {
        "square_footage": 0,
        "stories": 1,
        "siding": "Brick",
        "cleaning": "Soap/Scrub",
        "small_overhangs": 0,
        "medium_decks": 0,
        "ladder_spots_house": 0,
        "ladder_spots_pest": 0,
        "rodent_stations": 0,
        "exterior_standard_windows": 0,
        "exterior_high_windows": 0,
        "interior_standard_windows": 0,
        "interior_high_windows": 0,
        "tracks_sills_price": 0,
    }

if "results" not in st.session_state:
    st.session_state.results = {}

# Title
st.title("CC Inc. Pricing Calculator")

# Account Name
account_name = st.text_input("Account Name", placeholder="Enter account name (e.g., Rizzo)")

# Customer Information
st.header("Customer Information")
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
address = st.text_input("Address")

customer_info = {
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "phone": phone,
    "address": address,
}

# Estimate Details
st.header("Estimate Details")

# House Washing
st.subheader("House Washing")
square_footage = st.number_input("Square Footage", min_value=0, step=100, key="square_footage")
stories = st.number_input("Stories", min_value=1, max_value=5, step=1, key="stories")
siding = st.selectbox("Siding", ["Brick", "Vinyl", "Stucco", "Wood", "Aluminum"], key="siding")
cleaning = st.selectbox("Cleaning", ["Soap/Scrub", "Soft Wash", "Pressure Wash", "Chemical Wash"], key="cleaning")
small_overhangs = st.number_input("Small Overhangs", min_value=0, step=1, key="small_overhangs")
medium_decks = st.number_input("Medium Decks", min_value=0, step=1, key="medium_decks")
ladder_spots_house = st.number_input("Ladder Spots (House Washing)", min_value=0, step=1, key="ladder_spots_house")

# Pest Control
st.subheader("Pest Control")
ladder_spots_pest = st.number_input("Ladder Spots (Pest Control)", min_value=0, step=1, key="ladder_spots_pest")
rodent_stations = st.number_input("Rodent Stations", min_value=0, step=1, key="rodent_stations")

# Window Cleaning
st.subheader("Window Cleaning")
exterior_standard_windows = st.number_input("Exterior Standard Windows", min_value=0, step=1, key="exterior_standard_windows")
exterior_high_windows = st.number_input("Exterior High Windows", min_value=0, step=1, key="exterior_high_windows")
interior_standard_windows = st.number_input("Interior Standard Windows", min_value=0, step=1, key="interior_standard_windows")
interior_high_windows = st.number_input("Interior High Windows", min_value=0, step=1, key="interior_high_windows")
tracks_sills_price = st.number_input("Tracks/Sills Price", min_value=0.0, step=1.0, key="tracks_sills_price")

# Calculate Button
if st.button("Calculate"):
    # House Washing Calculation
    base_price = 199.00
    square_footage_price = square_footage * 0.04
    stories_price = (stories - 1) * 50.00
    siding_multipliers = {"Brick": 1.0, "Vinyl": 1.1, "Stucco": 1.2, "Wood": 1.3, "Aluminum": 1.4}
    siding_price = (base_price + square_footage_price + stories_price) * siding_multipliers[siding]
    cleaning_multipliers = {"Soap/Scrub": 1.0, "Soft Wash": 1.2, "Pressure Wash": 1.5, "Chemical Wash": 1.8}
    cleaning_price = siding_price * cleaning_multipliers[cleaning]
    small_overhangs_price = small_overhangs * 25.00
    medium_decks_price = medium_decks * 50.00
    ladder_spots_house_price = ladder_spots_house * 25.00
    house_washing_total = cleaning_price + small_overhangs_price + medium_decks_price + ladder_spots_house_price

    # Pest Control Calculation
    pest_base_price = 99.00
    ladder_spots_pest_price = ladder_spots_pest * 25.00
    pest_control_total = pest_base_price + ladder_spots_pest_price

    # Rodent Control Calculation
    rodent_base_price = 199.00
    rodent_stations_price = rodent_stations * 50.00
    rodent_control_total = rodent_base_price + rodent_stations_price

    # Window Cleaning Calculation
    exterior_standard_windows_price = exterior_standard_windows * 5.00
    exterior_high_windows_price = exterior_high_windows * 10.00
    interior_standard_windows_price = interior_standard_windows * 5.00
    interior_high_windows_price = interior_high_windows * 10.00
    windows_total = (exterior_standard_windows_price + exterior_high_windows_price +
                     interior_standard_windows_price + interior_high_windows_price)
    tracks_sills_total = tracks_sills_price

    # Total Estimate
    total_estimate = house_washing_total + pest_control_total + rodent_control_total + windows_total + tracks_sills_total

    # Store results in session state
    st.session_state.results = {
        "house_washing": round(house_washing_total, 2),
        "pest_control": round(pest_control_total, 2),
        "rodent_control": round(rodent_control_total, 2),
        "windows": round(windows_total, 2),
        "tracks_sills": round(tracks_sills_total, 2),
        "total": round(total_estimate, 2),
    }

    # Update inputs in session state
    st.session_state.inputs.update({
        "square_footage": square_footage,
        "stories": stories,
        "siding": siding,
        "cleaning": cleaning,
        "small_overhangs": small_overhangs,
        "medium_decks": medium_decks,
        "ladder_spots_house": ladder_spots_house,
        "ladder_spots_pest": ladder_spots_pest,
        "rodent_stations": rodent_stations,
        "exterior_standard_windows": exterior_standard_windows,
        "exterior_high_windows": exterior_high_windows,
        "interior_standard_windows": interior_standard_windows,
        "interior_high_windows": interior_high_windows,
        "tracks_sills_price": tracks_sills_price,
    })

# Display Results
if st.session_state.results:
    st.header("Pricing Estimate")
    st.write(f"house washing: {st.session_state.results['house_washing']}")
    st.write(f"pest control: {st.session_state.results['pest_control']}")
    st.write(f"rodent control: {st.session_state.results['rodent_control']}")
    st.write(f"windows: {st.session_state.results['windows']}")
    st.write(f"interior windows: {st.session_state.results['windows']}")
    st.write(f"tracks and sills: {st.session_state.results['tracks_sills']}")
    st.write(f"**TOTAL: {st.session_state.results['total']}**")

    # Save Estimate Button
    if st.button("Save Estimate"):
        if not account_name:
            st.error("Please enter an account name before saving.")
        else:
            save_estimate(account_name, customer_info, st.session_state.inputs, st.session_state.results)

# Additional Services
st.header("Would you like any additional services?")
additional_services = st.selectbox("Select additional services:", ["None", "Gutter Cleaning", "Driveway Cleaning", "Roof Cleaning"])
if additional_services != "None":
    st.write(f"Additional service selected: {additional_services}")
