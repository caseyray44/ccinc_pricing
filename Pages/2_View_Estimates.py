import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="View Saved Estimates", layout="wide")

# Google Sheets setup
def get_google_sheets_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["GOOGLE_CREDENTIALS"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client

def load_estimates():
    client = get_google_sheets_client()
    spreadsheet_id = st.secrets["SPREADSHEET_ID"]
    sheet = client.open_by_key(spreadsheet_id).sheet1
    records = sheet.get_all_records()
    return records

def delete_estimate(account_name):
    client = get_google_sheets_client()
    spreadsheet_id = st.secrets["SPREADSHEET_ID"]
    sheet = client.open_by_key(spreadsheet_id).sheet1
    all_records = sheet.get_all_records()
    row_to_delete = None
    for idx, record in enumerate(all_records, start=2):
        if record["Account Name"] == account_name:
            row_to_delete = idx
            break
    if row_to_delete:
        sheet.delete_rows(row_to_delete)

# Title
st.title("View Saved Estimates")

# Load estimates
try:
    estimates = load_estimates()
except Exception as e:
    st.error(f"Failed to load estimates: {str(e)}")
    estimates = []

if not estimates:
    st.write("No estimates found.")
else:
    # Dropdown to select an estimate
    account_names = [estimate["Account Name"] for estimate in estimates]
    selected_account = st.selectbox("Select an estimate to view:", account_names)

    # Find the selected estimate
    selected_estimate = next((e for e in estimates if e["Account Name"] == selected_account), None)

    if selected_estimate:
        customer_info = json.loads(selected_estimate["Customer Info"])
        inputs = json.loads(selected_estimate["Inputs"])
        results = json.loads(selected_estimate["Results"])

        # Display Customer Information
        st.header("Customer Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"First Name: {customer_info['first_name']}")
            st.write(f"Last Name: {customer_info['last_name']}")
        with col2:
            st.write(f"Email: {customer_info['email']}")
            st.write(f"Phone: {customer_info['phone']}")
        st.write(f"Address: {customer_info['address']}")

        # Display Estimate Details
        st.header("Estimate Details")
        st.subheader("House Washing")
        col3, col4, col5 = st.columns(3)
        with col3:
            st.write(f"Square Footage: {inputs['square_footage']}")
        with col4:
            st.write(f"Stories: {inputs['stories']}")
        with col5:
            st.write(f"Siding: {inputs['siding']}")

        col6, col7 = st.columns(2)
        with col6:
            st.write(f"Cleaning: {inputs['cleaning']}")
        with col7:
            st.write(f"Small Overhangs: {inputs['small_overhangs']}")

        col8, col9 = st.columns(2)
        with col8:
            st.write(f"Medium Decks: {inputs['medium_decks']}")
        with col9:
            st.write(f"Ladder Spots (House Washing): {inputs['ladder_spots_house']}")

        st.subheader("Pest Control")
        col10, col11 = st.columns(2)
        with col10:
            st.write(f"Ladder Spots (Pest Control): {inputs['ladder_spots_pest']}")
        with col11:
            st.write(f"Rodent Stations: {inputs['rodent_stations']}")

        st.subheader("Window Cleaning")
        col12, col13 = st.columns(2)
        with col12:
            st.write(f"Exterior Standard Windows: {inputs['exterior_standard_windows']}")
            st.write(f"Exterior High Windows: {inputs['exterior_high_windows']}")
        with col13:
            st.write(f"Interior Standard Windows: {inputs['interior_standard_windows']}")
            st.write(f"Interior High Windows: {inputs['interior_high_windows']}")

        st.write(f"Tracks/Sills Price: {inputs['tracks_sills_price']}")

        # Display Results
        st.header("Pricing Estimate")
        st.write(f"house washing: {results['house_washing']}")
        st.write(f"pest control: {results['pest_control']}")
        st.write(f"rodent control: {results['rodent_control']}")
        st.write(f"windows: {results['windows']}")
        st.write(f"tracks and sills: {results['tracks_sills']}")
        st.write(f"**Total: {results['total']}**")

        # Edit and Delete Buttons
        col14, col15 = st.columns(2)
        with col14:
            if st.button("Edit Estimate"):
                st.session_state["edit_mode"] = True
                st.session_state["edit_account_name"] = selected_account
                st.session_state["edit_customer_info"] = customer_info
                st.session_state["edit_inputs"] = inputs
                st.session_state["edit_results"] = results
                st.experimental_rerun()

        with col15:
            if st.button("Delete Estimate"):
                delete_estimate(selected_account)
                st.success(f"Estimate for {selected_account} deleted!")
                st.experimental_rerun()

# Edit Mode
if "edit_mode" in st.session_state and st.session_state["edit_mode"]:
    st.header("Edit Estimate")
    account_name = st.session_state["edit_account_name"]
    customer_info = st.session_state["edit_customer_info"]
    inputs = st.session_state["edit_inputs"]

    st.subheader("Customer Information")
    col16, col17 = st.columns(2)
    with col16:
        first_name = st.text_input("First Name", value=customer_info["first_name"])
        last_name = st.text_input("Last Name", value=customer_info["last_name"])
    with col17:
        email = st.text_input("Email", value=customer_info["email"])
        phone = st.text_input("Phone", value=customer_info["phone"])
    address = st.text_input("Address", value=customer_info["address"])

    updated_customer_info = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "address": address,
    }

    st.subheader("Estimate Details")
    st.subheader("House Washing")
    col18, col19, col20 = st.columns(3)
    with col18:
        square_footage = st.number_input("Square Footage", min_value=0, step=100, value=inputs["square_footage"])
    with col19:
        stories = st.number_input("Stories", min_value=1, max_value=5, step=1, value=inputs["stories"])
    with col20:
        siding = st.selectbox("Siding", ["Brick", "Vinyl", "Stucco"], index=["Brick", "Vinyl", "Stucco"].index(inputs["siding"]))

    col21, col22 = st.columns(2)
    with col21:
        cleaning = st.selectbox("Cleaning", ["Soap/Scrub", "Soft Wash", "Pressure Wash"], index=["Soap/Scrub", "Soft Wash", "Pressure Wash"].index(inputs["cleaning"]))
    with col22:
        small_overhangs = st.number_input("Small Overhangs", min_value=0, step=1, value=inputs["small_overhangs"])

    col23, col24 = st.columns(2)
    with col23:
        medium_decks = st.number_input("Medium Decks", min_value=0, step=1, value=inputs["medium_decks"])
    with col24:
        ladder_spots_house = st.number_input("Ladder Spots (House Washing)", min_value=0, step=1, value=inputs["ladder_spots_house"])

    st.subheader("Pest Control")
    col25, col26 = st.columns(2)
    with col25:
        ladder_spots_pest = st.number_input("Ladder Spots (Pest Control)", min_value=0, step=1, value=inputs["ladder_spots_pest"])
    with col26:
        rodent_stations = st.number_input("Rodent Stations", min_value=0, step=1, value=inputs["rodent_stations"])

    st.subheader("Window Cleaning")
    col27, col28 = st.columns(2)
    with col27:
        exterior_standard_windows = st.number_input("Exterior Standard Windows", min_value=0, step=1, value=inputs["exterior_standard_windows"])
        exterior_high_windows = st.number_input("Exterior High Windows", min_value=0, step=1, value=inputs["exterior_high_windows"])
    with col28:
        interior_standard_windows = st.number_input("Interior Standard Windows", min_value=0, step=1, value=inputs["interior_standard_windows"])
        interior_high_windows = st.number_input("Interior High Windows", min_value=0, step=1, value=inputs["interior_high_windows"])

    tracks_sills_price = st.number_input("Tracks/Sills Price", min_value=0.0, step=1.0, value=inputs["tracks_sills_price"])

    if st.button("Calculate and Save Updated Estimate"):
        # Recalculate the estimate
        base_price = 199.00
        square_footage_price = square_footage * 0.04
        stories_price = (stories - 1) * 50.00
        siding_multipliers = {"Brick": 1.0, "Vinyl": 1.1, "Stucco": 1.2}
        siding_price = (base_price + square_footage_price + stories_price) * siding_multipliers[siding]
        cleaning_multipliers = {"Soap/Scrub": 1.0, "Soft Wash": 1.2, "Pressure Wash": 1.5}
        cleaning_price = siding_price * cleaning_multipliers[cleaning]
        small_overhangs_price = small_overhangs * 25.00
        medium_decks_price = medium_decks * 50.00
        ladder_spots_house_price = ladder_spots_house * 25.00
        house_washing_total = cleaning_price + small_overhangs_price + medium_decks_price + ladder_spots_house_price

        pest_base_price = 99.00
        ladder_spots_pest_price = ladder_spots_pest * 25.00
        pest_control_total = pest_base_price + ladder_spots_pest_price

        rodent_base_price = 199.00
        rodent_stations_price = rodent_stations * 50.00
        rodent_control_total = rodent_base_price + rodent_stations_price

        exterior_standard_windows_price = exterior_standard_windows * 5.00
        exterior_high_windows_price = exterior_high_windows * 10.00
        interior_standard_windows_price = interior_standard_windows * 5.00
        interior_high_windows_price = interior_high_windows * 10.00
        windows_total = (exterior_standard_windows_price + exterior_high_windows_price +
                         interior_standard_windows_price + interior_high_windows_price)
        tracks_sills_total = tracks_sills_price

        total_estimate = house_washing_total + pest_control_total + rodent_control_total + windows_total + tracks_sills_total

        updated_results = {
            "house_washing": round(house_washing_total, 2),
            "pest_control": round(pest_control_total, 2),
            "rodent_control": round(rodent_control_total, 2),
            "windows": round(windows_total, 2),
            "tracks_sills": round(tracks_sills_total, 2),
            "total": round(total_estimate, 2),
        }

        updated_inputs = {
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
        }

        # Save the updated estimate
        client = get_google_sheets_client()
        spreadsheet_id = st.secrets["SPREADSHEET_ID"]
        sheet = client.open_by_key(spreadsheet_id).sheet1
        all_records = sheet.get_all_records()
        row_to_update = None
        for idx, record in enumerate(all_records, start=2):
            if record["Account Name"] == account_name:
                row_to_update = idx
                break

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        customer_info_str = json.dumps(updated_customer_info)
        inputs_str = json.dumps(updated_inputs)
        results_str = json.dumps(updated_results)

        if row_to_update:
            sheet.update(f"A{row_to_update}:E{row_to_update}", [[account_name, timestamp, customer_info_str, inputs_str, results_str]])
            st.success(f"Updated estimate for {account_name} saved to Google Sheets!")
            st.session_state["edit_mode"] = False
            st.experimental_rerun()
        else:
            st.error("Estimate not found for updating.")
