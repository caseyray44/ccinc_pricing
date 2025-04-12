import streamlit as st
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Inject custom CSS to hide sidebar page titles on mobile
st.markdown(
    """
    <style>
    @media (max-width: 768px) {
        div[data-testid="stSidebarNavItems"] > div {
            display: none !important;
        }
        div[data-testid="stSidebarNav"] {
            display: block !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Google Sheets setup
def get_google_sheets_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client

def save_estimate(account_name, inputs, results):
    try:
        client = get_google_sheets_client()
        spreadsheet_id = st.secrets["SPREADSHEET_ID"]
        st.write(f"Using Spreadsheet ID: {spreadsheet_id}")
        sheet = client.open_by_key(spreadsheet_id).sheet1
        all_records = sheet.get_all_records()
        row_to_update = None
        for idx, record in enumerate(all_records, start=2):
            if record["Account Name"] == account_name:
                row_to_update = idx
                break
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        inputs_str = json.dumps(inputs)
        results_str = json.dumps(results)
        st.write(f"Saving inputs: {inputs_str}")
        st.write(f"Saving results: {results_str}")
        if row_to_update:
            sheet.update(f"A{row_to_update}:D{row_to_update}", [[account_name, timestamp, inputs_str, results_str]])
        else:
            sheet.append_row([account_name, timestamp, inputs_str, results_str])
        st.success(f"Estimate for {account_name} saved to Google Sheets!")
    except Exception as e:
        st.error(f"Failed to save estimate. Error: {str(e)}")
        raise e

# Initialize session state
if "inputs" not in st.session_state:
    st.session_state.inputs = {
        "total_perimeter": 0,
        "max_height": 0,
        "house_dirtiness": "Light",
        "stories": 1.0,
        "pest_infestation": "Light",
        "ladder_spots_pest": 0,
        "structure_type": "Main",
        "rodent_stations": 4,
        "interior_monitoring": False,
        "include_exterior_windows": False,
        "exterior_standard_windows": 0,
        "exterior_high_windows": 0,
        "include_interior_windows": False,
        "interior_standard_windows": 0,
        "interior_high_windows": 0,
        "tracks_sills_price": 99.0,
        "roof_treatment": "NO",
        "roof_type": "Asphalt",
        "roof_sq_ft": 0,
        "roof_metal_min": 399.0,
        "gutter_cleaning": "NO",
        "gutter_linear_feet": 0,
        "roof_blow_off": "NO",
        "blow_off_hours": 0,
        "blow_off_men": 1,
        "concrete_cleaning": "NO",
        "concrete_sq_ft": 0,
        "deck_dock_cleaning": "NO",
        "deck_dock_sq_ft": 0,
        "custom_items": [],
    }

if "results" not in st.session_state:
    st.session_state.results = {}

# Display pricing estimate
def display_pricing_estimate():
    if st.session_state.results:
        st.header("Pricing Estimate")
        for service in ["house_washing", "pest_control", "rodent_control", "exterior_windows", "interior_windows", "tracks_sills"]:
            if service in st.session_state.results:
                st.write(f"{service.replace('_', ' ')}: ${st.session_state.results[service]:.2f}")
        for service, price in st.session_state.results.items():
            if service not in ["house_washing", "pest_control", "rodent_control", "exterior_windows", "interior_windows", "tracks_sills", "total"]:
                st.write(f"{service}: ${price:.2f}")
        if "total" in st.session_state.results:
            st.write(f"**TOTAL: ${st.session_state.results['total']:.2f}**")

# Title
st.title("CC Inc. Pricing Calculator")

# Account Name
account_name = st.text_input("Account Name", placeholder="Enter account name (e.g., Rizzo)")

# Estimate Details
st.header("Estimate Details")

# Shared Inputs for House Washing and Pest Control
st.subheader("Property Measurements")
total_perimeter = st.number_input("Total Perimeter (ft)", min_value=0.0, step=1.0, key="total_perimeter")
stories = st.selectbox("Number of Stories", [1.0, 1.5, 2.0, 2.5, 3.0], key="stories")

# House Washing
st.subheader("House Washing")
max_height = st.number_input("Max Height (ft)", min_value=0.0, step=1.0, key="max_height")
house_dirtiness = st.radio("Dirtiness", ["Light", "Medium", "Heavy"], key="house_dirtiness")

# Pest Control
st.subheader("Pest Control")
pest_infestation = st.radio("Infestation Level", ["Light", "Medium", "Heavy"], key="pest_infestation")
ladder_spots_pest = st.number_input("Ladder Spots (Pest Control)", min_value=0, step=1, key="ladder_spots_pest")
structure_type = st.radio("Structure Type", ["Main", "Additional"], key="structure_type")

# Rodent Control (Unchanged)
st.subheader("Rodent Control")
rodent_stations = st.number_input("Rodent Stations", min_value=0, step=1, value=4, key="rodent_stations")
interior_monitoring = st.checkbox("Interior Monitoring", key="interior_monitoring")

# Window Cleaning (Updated)
st.subheader("Window Cleaning")
include_exterior_windows = st.checkbox("Include Exterior Window Cleaning", key="include_exterior_windows")
if include_exterior_windows:
    exterior_standard_windows = st.number_input("Exterior Standard Windows", min_value=0, step=1, key="exterior_standard_windows")
    exterior_high_windows = st.number_input("Exterior High Windows", min_value=0, step=1, key="exterior_high_windows")
else:
    exterior_standard_windows = 0
    exterior_high_windows = 0

include_interior_windows = st.checkbox("Include Interior Window Cleaning", key="include_interior_windows")
if include_interior_windows:
    interior_standard_windows = st.number_input("Interior Standard Windows", min_value=0, step=1, key="interior_standard_windows")
    interior_high_windows = st.number_input("Interior High Windows", min_value=0, step=1, key="interior_high_windows")
else:
    interior_standard_windows = 0
    interior_high_windows = 0

tracks_sills_price = st.number_input("Tracks/Sills Price (minimum $99)", min_value=0.0, step=1.0, value=99.0, key="tracks_sills_price")

# Calculate Button
if st.button("Calculate"):
    missing_details = []
    if total_perimeter == 0:
        missing_details.append("total perimeter")
    if max_height == 0:
        missing_details.append("max height for house washing")
    if tracks_sills_price == 0:
        missing_details.append("tracks/sills price (or confirm to use default $99)")

    if missing_details:
        st.error(f"I need more information to calculate the prices. Please provide: {', '.join(missing_details)}.")
    else:
        # House Washing Calculation
        house_sq_ft = total_perimeter * max_height
        if house_sq_ft < 6000:
            house_base_rate = 0.094
        else:
            house_base_rate = 0.101
        house_condition_adder = 0
        if house_dirtiness == "Medium":
            house_condition_adder = 76
        elif house_dirtiness == "Heavy":
            house_condition_adder = 152
        house_washing_total = (house_sq_ft * house_base_rate) + house_condition_adder
        house_washing_total = max(house_washing_total, 449)  # Updated minimum price

        # Pest Control Calculation
        treated_area = total_perimeter * (stories * 10)
        if treated_area < 6000:
            pest_base_rate = 0.049 if structure_type == "Additional" else 0.033
        else:
            pest_base_rate = 0.023
        pest_infestation_adder = 0
        if pest_infestation == "Medium":
            pest_infestation_adder = 50
        elif pest_infestation == "Heavy":
            pest_infestation_adder = 100
        ladder_cost = 25 if ladder_spots_pest > 0 else 0
        ladder_cost += (ladder_spots_pest - 1) * 15 if ladder_spots_pest > 1 else 0
        pest_total = (treated_area * pest_base_rate) + pest_infestation_adder + ladder_cost
        if structure_type == "Main":
            pest_minimum_price = 179 if treated_area < 3000 else 145
            pest_total = max(pest_total, pest_minimum_price)

        # Rodent Control Calculation (Unchanged)
        rodent_base_price = 399.00
        extra_stations = max(0, rodent_stations - 4)
        rodent_stations_price = extra_stations * 30.00
        interior_monitoring_price = 50.00 if interior_monitoring else 0.00
        rodent_control_total = rodent_base_price + rodent_stations_price + interior_monitoring_price

        # Window Cleaning Calculation (Updated)
        if include_exterior_windows:
            exterior_windows_total = (exterior_standard_windows * 3.30) + (exterior_high_windows * 5.25)
            exterior_windows_total = max(exterior_windows_total, 149.00)  # Always apply minimum
        else:
            exterior_windows_total = 0.00

        if include_interior_windows:
            interior_windows_total = (interior_standard_windows * 2.00) + (interior_high_windows * 4.00)
            interior_windows_total = max(interior_windows_total, 99.00)  # Always apply minimum
        else:
            interior_windows_total = 0.00

        tracks_sills_total = tracks_sills_price if tracks_sills_price > 0 else 99.00

        # Store mandatory results
        results = {
            "house_washing": round(house_washing_total, 2),
            "pest_control": round(pest_total, 2),
            "rodent_control": round(rodent_control_total, 2),
            "exterior_windows": round(exterior_windows_total, 2),
            "interior_windows": round(interior_windows_total, 2),
            "tracks_sills": round(tracks_sills_total, 2),
        }

        # Calculate initial total
        total = sum(results.values())
        results["total"] = round(total, 2)

        # Update inputs in session state
        st.session_state.inputs.update({
            "total_perimeter": total_perimeter,
            "max_height": max_height,
            "house_dirtiness": house_dirtiness,
            "stories": stories,
            "pest_infestation": pest_infestation,
            "ladder_spots_pest": ladder_spots_pest,
            "structure_type": structure_type,
            "rodent_stations": rodent_stations,
            "interior_monitoring": interior_monitoring,
            "include_exterior_windows": include_exterior_windows,
            "exterior_standard_windows": exterior_standard_windows,
            "exterior_high_windows": exterior_high_windows,
            "include_interior_windows": include_interior_windows,
            "interior_standard_windows": interior_standard_windows,
            "interior_high_windows": interior_high_windows,
            "tracks_sills_price": tracks_sills_price,
        })

        # Store results in session state
        st.session_state.results = results

        # Display the initial pricing estimate
        display_pricing_estimate()

        # Show the additional services prompt
        st.session_state.show_additional_services = True

# Additional Services (Unchanged)
if "show_additional_services" in st.session_state and st.session_state.show_additional_services:
    st.header("Would you like any additional services? (roof treatment, gutter cleaning, roof blow-off, concrete cleaning, deck/dock cleaning, custom items)")
    additional_services = st.multiselect("Select additional services:", [
        "roof treatment", "gutter cleaning", "roof blow-off", "concrete cleaning", "deck/dock cleaning", "custom items"
    ])

    additional_results = {}
    if additional_services:
        for service in additional_services:
            if service == "roof treatment":
                roof_type = st.selectbox("Roof Type", ["Asphalt", "Metal"], key="roof_type")
                roof_sq_ft = st.number_input("Roof Square Footage", min_value=0, step=100, key="roof_sq_ft")
                roof_metal_min = st.number_input("Metal Roof Minimum (399 or 599)", min_value=399.0, step=1.0, value=399.0, key="roof_metal_min") if roof_type == "Metal" else 399.0
                if roof_sq_ft == 0:
                    st.error("I need more information to calculate the prices. Please provide: roof square footage.")
                    continue
                rate = 0.25 if roof_type == "Asphalt" else 0.85
                min_price = 399.0 if roof_type == "Asphalt" else roof_metal_min
                roof_price = roof_sq_ft * rate
                roof_price = max(roof_price, min_price)
                additional_results["roof treatment"] = round(roof_price, 2)
                st.session_state.inputs.update({
                    "roof_treatment": "YES",
                    "roof_type": roof_type,
                    "roof_sq_ft": roof_sq_ft,
                    "roof_metal_min": roof_metal_min,
                })
            elif service == "gutter cleaning":
                gutter_linear_feet = st.number_input("Gutter Linear Feet", min_value=0, step=1, key="gutter_linear_feet")
                if gutter_linear_feet == 0:
                    st.error("I need more information to calculate the prices. Please provide: gutter linear feet.")
                    continue
                gutter_price = gutter_linear_feet * 0.50
                gutter_price = max(gutter_price, 149.00)
                additional_results["gutter cleaning"] = round(gutter_price, 2)
                st.session_state.inputs.update({
                    "gutter_cleaning": "YES",
                    "gutter_linear_feet": gutter_linear_feet,
                })
            elif service == "roof blow-off":
                blow_off_hours = st.number_input("Hours for Roof Blow-Off", min_value=0, step=1, key="blow_off_hours")
                blow_off_men = st.selectbox("Number of Men", [1, 2], key="blow_off_men")
                if blow_off_hours == 0:
                    st.error("I need more information to calculate the prices. Please provide: hours for roof blow-off.")
                    continue
                blow_off_price = (blow_off_hours * 149.00) + (blow_off_hours * 42.00 if blow_off_men == 2 else 0)
                additional_results["roof blow-off"] = round(blow_off_price, 2)
                st.session_state.inputs.update({
                    "roof_blow_off": "YES",
                    "blow_off_hours": blow_off_hours,
                    "blow_off_men": blow_off_men,
                })
            elif service == "concrete cleaning":
                concrete_sq_ft = st.number_input("Concrete Square Footage", min_value=0, step=100, key="concrete_sq_ft")
                if concrete_sq_ft == 0:
                    st.error("I need more information to calculate the prices. Please provide: concrete square footage.")
                    continue
                concrete_price = concrete_sq_ft * 0.15
                additional_results["concrete cleaning"] = round(concrete_price, 2)
                st.session_state.inputs.update({
                    "concrete_cleaning": "YES",
                    "concrete_sq_ft": concrete_sq_ft,
                })
            elif service == "deck/dock cleaning":
                deck_dock_sq_ft = st.number_input("Deck/Dock Square Footage", min_value=0, step=100, key="deck_dock_sq_ft")
                if deck_dock_sq_ft == 0:
                    st.error("I need more information to calculate the prices. Please provide: deck/dock square footage.")
                    continue
                deck_dock_price = deck_dock_sq_ft * 0.15
                additional_results["deck/dock cleaning"] = round(deck_dock_price, 2)
                st.session_state.inputs.update({
                    "deck_dock_cleaning": "YES",
                    "deck_dock_sq_ft": deck_dock_sq_ft,
                })
            elif service == "custom items":
                custom_item_name = st.text_input("Custom Item Name", key="custom_item_name")
                custom_item_price = st.number_input("Custom Item Price", min_value=0.0, step=1.0, key="custom_item_price")
                if not custom_item_name or custom_item_price == 0:
                    st.error("I need more information to calculate the prices. Please provide: custom item name and price.")
                    continue
                custom_item = {"name": custom_item_name, "price": custom_item_price}
                st.session_state.inputs["custom_items"].append(custom_item)
                additional_results[f"custom line item ({custom_item_name})"] = round(custom_item_price, 2)

        if additional_results:
            st.session_state.results.update(additional_results)
            total = sum(st.session_state.results.values()) - st.session_state.results.get("total", 0)
            st.session_state.results["total"] = round(total, 2)
        display_pricing_estimate()

# Save Estimate Button
if st.session_state.results:
    if st.button("Save Estimate"):
        if not account_name:
            st.error("Please enter an account name before saving.")
        else:
            save_estimate(account_name, st.session_state.inputs, st.session_state.results)
