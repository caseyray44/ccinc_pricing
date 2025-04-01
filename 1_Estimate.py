import streamlit as st
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Inject custom CSS to hide sidebar page titles on mobile for this page
st.markdown(
    """
    <style>
    /* Hide sidebar page titles on mobile (screen width <= 768px) */
    @media (max-width: 768px) {
        /* Target the container of the page titles in mobile view */
        div[data-testid="stSidebarNavItems"] > div {
            display: none !important;
        }
        /* Ensure the hamburger menu remains visible */
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
        inputs_str = json.dumps(inputs)
        results_str = json.dumps(results)
        # Debug: Log the data being saved
        st.write(f"Saving inputs: {inputs_str}")
        st.write(f"Saving results: {results_str}")

        # If the account name exists, update the existing row; otherwise, append a new row
        if row_to_update:
            sheet.update(f"A{row_to_update}:D{row_to_update}", [[account_name, timestamp, inputs_str, results_str]])
        else:
            sheet.append_row([account_name, timestamp, inputs_str, results_str])
        st.success(f"Estimate for {account_name} saved to Google Sheets!")
    except Exception as e:
        st.error(f"Failed to save estimate. Error: {str(e)}")
        raise e

# Initialize session state for inputs
if "inputs" not in st.session_state:
    st.session_state.inputs = {
        "square_footage": 0,
        "stories": 1.0,
        "siding": "Brick",
        "cleaning": "Soap/Scrub",
        "small_overhangs": 0,
        "medium_overhangs": 0,
        "large_overhangs": 0,
        "small_decks": 0,
        "medium_decks": 0,
        "large_decks": 0,
        "ladder_work": "NO",
        "ladder_spots_house": 0,
        "ladder_spots_pest": 0,
        "rodent_stations": 4,
        "interior_monitoring": False,
        "exterior_standard_windows": 0,
        "exterior_high_windows": 0,
        "interior_standard_windows": 0,
        "interior_high_windows": 0,
        "tracks_sills_price": 99.0,
        # Additional services
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

# Function to display the pricing estimate
def display_pricing_estimate():
    if st.session_state.results:
        st.header("Pricing Estimate")
        # Mandatory services (always display these if they exist)
        for service in ["house_washing", "pest_control", "rodent_control", "exterior_windows", "interior_windows", "tracks_sills"]:
            if service in st.session_state.results:
                st.write(f"{service.replace('_', ' ')}: {st.session_state.results[service]}")
        # Additional services
        for service, price in st.session_state.results.items():
            if service not in ["house_washing", "pest_control", "rodent_control", "exterior_windows", "interior_windows", "tracks_sills", "total"]:
                st.write(f"{service}: {price}")
        # Total
        if "total" in st.session_state.results:
            st.write(f"**TOTAL: {st.session_state.results['total']}**")

# Title
st.title("CC Inc. Pricing Calculator")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("How to Count Windows"):
        navigate_to("how_to_count_windows")
with col2:
    if st.button("View Estimates"):
        navigate_to("view_estimates")

# Account Name
account_name = st.text_input("Account Name", placeholder="Enter account name (e.g., Rizzo)")

# Estimate Details
st.header("Estimate Details")

# House Washing
st.subheader("House Washing")
square_footage = st.number_input("Square Footage", min_value=0, step=100, key="square_footage")
stories = st.selectbox("Stories", [1.0, 1.5, 2.0, 2.5, 3.0], key="stories")
siding = st.selectbox("Siding", ["Brick", "Metal", "Vinyl", "Shiplap", "Hardie/LP", "Log/Half-Log"], key="siding")
cleaning = st.selectbox("Cleaning", ["Soap/Scrub", "SH"], key="cleaning")
small_overhangs = st.number_input("Small Overhangs", min_value=0, step=1, key="small_overhangs")
medium_overhangs = st.number_input("Medium Overhangs", min_value=0, step=1, key="medium_overhangs")
large_overhangs = st.number_input("Large Overhangs", min_value=0, step=1, key="large_overhangs")
small_decks = st.number_input("Small Decks", min_value=0, step=1, key="small_decks")
medium_decks = st.number_input("Medium Decks", min_value=0, step=1, key="medium_decks")
large_decks = st.number_input("Large Decks", min_value=0, step=1, key="large_decks")
ladder_work = st.selectbox("Ladder Work Required?", ["NO", "YES"], key="ladder_work")
ladder_spots_house = st.number_input("Ladder Spots (House Washing)", min_value=0, step=1, key="ladder_spots_house") if ladder_work == "YES" else 0

# Pest Control
st.subheader("Pest Control")
ladder_spots_pest = st.number_input("Ladder Spots (Pest Control)", min_value=0, step=1, key="ladder_spots_pest")

# Rodent Control
st.subheader("Rodent Control")
rodent_stations = st.number_input("Rodent Stations", min_value=0, step=1, value=4, key="rodent_stations")
interior_monitoring = st.checkbox("Interior Monitoring", key="interior_monitoring")

# Window Cleaning
st.subheader("Window Cleaning")
exterior_standard_windows = st.number_input("Exterior Standard Windows", min_value=0, step=1, key="exterior_standard_windows")
exterior_high_windows = st.number_input("Exterior High Windows", min_value=0, step=1, key="exterior_high_windows")
interior_standard_windows = st.number_input("Interior Standard Windows", min_value=0, step=1, key="interior_standard_windows")
interior_high_windows = st.number_input("Interior High Windows", min_value=0, step=1, key="interior_high_windows")
tracks_sills_price = st.number_input("Tracks/Sills Price (minimum $99)", min_value=0.0, step=1.0, value=99.0, key="tracks_sills_price")

# Calculate Button
if st.button("Calculate"):
    # Input Validation
    missing_details = []
    # House Washing
    if square_footage == 0:
        missing_details.append("square footage for house washing")
    if not siding:
        missing_details.append("siding type for house washing")
    if not cleaning:
        missing_details.append("cleaning type for house washing")
    if ladder_work == "YES" and ladder_spots_house == 0:
        missing_details.append("number of ladder spots for house washing (since ladder work is YES)")
    # Window Cleaning
    if tracks_sills_price == 0:
        missing_details.append("tracks/sills price (or confirm to use default $99)")

    if missing_details:
        st.error(f"I need more information to calculate the prices. Please provide: {', '.join(missing_details)}.")
    else:
        # House Washing Calculation
        base_rate = 0.18 if cleaning == "Soap/Scrub" else 0.20
        siding_adjustments = {
            "Brick": 0.00, "Metal": 0.00, "Vinyl": 0.02, "Shiplap": 0.04,
            "Hardie/LP": 0.06, "Log/Half-Log": 0.08
        }
        adjusted_rate = base_rate + siding_adjustments[siding]
        base_price = square_footage * adjusted_rate
        story_multipliers = {1.0: 1.0, 1.5: 1.05, 2.0: 1.1, 2.5: 1.15, 3.0: 1.2}
        story_price = base_price * story_multipliers[stories]
        complexity_multiplier = 1.25 if (siding in ["Shiplap", "Log/Half-Log"] or ladder_work == "YES") else 1.0
        complexity_price = story_price * complexity_multiplier
        overhangs_price = (small_overhangs * 20.00) + (medium_overhangs * 30.00) + (large_overhangs * 40.00)
        decks_price = (small_decks * 15.00) + (medium_decks * 25.00) + (large_decks * 40.00)
        ladder_spots_house_price = ladder_spots_house * 75.00
        house_washing_total = complexity_price + overhangs_price + decks_price + ladder_spots_house_price
        if house_washing_total < 299.00:
            house_washing_total = 299.00

        # Pest Control Calculation
        base_price = square_footage * 0.045  # Reuse square footage from house washing
        base_price = min(base_price, 200.00)  # Cap at $200
        pest_overhangs_price = (small_overhangs * 15.00) + (medium_overhangs * 20.00) + (large_overhangs * 25.00)
        pest_decks_price = (small_decks * 10.00) + (medium_decks * 20.00) + (large_decks * 25.00)
        pest_ladder_price = ladder_spots_pest * 75.00
        pest_total = base_price + pest_overhangs_price + pest_decks_price + pest_ladder_price
        if pest_total < 119.00:
            pest_total = 119.00

        # Rodent Control Calculation
        rodent_base_price = 399.00
        extra_stations = max(0, rodent_stations - 4)
        rodent_stations_price = extra_stations * 30.00
        interior_monitoring_price = 50.00 if interior_monitoring else 0.00
        rodent_control_total = rodent_base_price + rodent_stations_price + interior_monitoring_price

        # Window Cleaning Calculation
        exterior_windows_total = (exterior_standard_windows * 3.30) + (exterior_high_windows * 5.25)
        if exterior_windows_total < 149.00:
            exterior_windows_total = 149.00
        interior_windows_total = (interior_standard_windows * 2.00) + (interior_high_windows * 4.00)
        if interior_windows_total < 99.00:
            interior_windows_total = 99.00
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
            "square_footage": square_footage,
            "stories": stories,
            "siding": siding,
            "cleaning": cleaning,
            "small_overhangs": small_overhangs,
            "medium_overhangs": medium_overhangs,
            "large_overhangs": large_overhangs,
            "small_decks": small_decks,
            "medium_decks": medium_decks,
            "large_decks": large_decks,
            "ladder_work": ladder_work,
            "ladder_spots_house": ladder_spots_house,
            "ladder_spots_pest": ladder_spots_pest,
            "rodent_stations": rodent_stations,
            "interior_monitoring": interior_monitoring,
            "exterior_standard_windows": exterior_standard_windows,
            "exterior_high_windows": exterior_high_windows,
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

# Additional Services
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

        # Update session state with additional results
        if additional_results:
            st.session_state.results.update(additional_results)
            # Recalculate total
            total = sum(st.session_state.results.values()) - st.session_state.results.get("total", 0)
            st.session_state.results["total"] = round(total, 2)

        # Display the updated pricing estimate
        display_pricing_estimate()

# Save Estimate Button (only show if there are results)
if st.session_state.results:
    if st.button("Save Estimate"):
        if not account_name:
            st.error("Please enter an account name before saving.")
        else:
            save_estimate(account_name, st.session_state.inputs, st.session_state.results)
