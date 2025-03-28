# 1_Estimate.py
import streamlit as st
import json
import os
from datetime import datetime

# Directory for saving estimates
ESTIMATES_DIR = "estimates"
if not os.path.exists(ESTIMATES_DIR):
    os.makedirs(ESTIMATES_DIR)

def calculate_house_washing(sq_ft, stories, siding, cleaning, small_overhangs, medium_overhangs, large_overhangs,
                           small_decks, medium_decks, large_decks, ladder_spots_hw):
    base_rate = 0.18 if cleaning == "Soap/Scrub" else 0.20
    base = sq_ft * base_rate
    siding_adj = {"Brick": 0.00, "Metal": 0.00, "Vinyl": 0.02, "Shiplap": 0.04, "Hardie/LP": 0.06, "Log/Half-Log": 0.08}[siding]
    adjusted_base = sq_ft * (base_rate + siding_adj)
    story_mult = {1: 1.0, 1.5: 1.05, 2: 1.1, 2.5: 1.15, 3: 1.2}[stories]
    subtotal = adjusted_base * story_mult
    complexity_mult = 1.25 if siding in ["Shiplap", "Log/Half-Log"] or ladder_spots_hw > 0 else 1.0
    subtotal *= complexity_mult
    overhang_fees = (small_overhangs * 20) + (medium_overhangs * 30) + (large_overhangs * 40)
    deck_fees = (small_decks * 15) + (medium_decks * 25) + (large_decks * 40)
    ladder_fees = ladder_spots_hw * 75
    flat_fees = overhang_fees + deck_fees + ladder_fees
    subtotal += flat_fees
    subtotal = max(299, subtotal)
    return subtotal

def calculate_pest_control(sq_ft, small_overhangs, medium_overhangs, large_overhangs,
                          small_decks, medium_decks, large_decks, ladder_spots_pc):
    base = sq_ft * 0.045
    overhang_fees = (small_overhangs * 15) + (medium_overhangs * 20) + (large_overhangs * 25)
    deck_fees = (small_decks * 10) + (medium_decks * 20) + (large_decks * 25)
    ladder_fees = ladder_spots_pc * 75
    flat_fees = overhang_fees + deck_fees + ladder_fees
    subtotal = base + flat_fees
    subtotal = max(119, subtotal)
    return subtotal

def calculate_rodent_control(stations, interior):
    base = 399
    extra_stations = max(0, stations - 4)
    extra_fees = extra_stations * 30
    interior_fee = 50 if interior else 0
    total = base + extra_fees + interior_fee
    return total

def calculate_windows(ext_standard, ext_high, int_standard, int_high, tracks_sills):
    ext_total = (ext_standard * 3.30) + (ext_high * 5.25)
    ext_total = max(149, ext_total)
    int_total = (int_standard * 2.00) + (int_high * 4.00)
    int_total = max(99, int_total)
    tracks_sills_total = tracks_sills if tracks_sills is not None else 99
    return ext_total, int_total, tracks_sills_total

def calculate_add_ons(add_ons):
    add_on_results = []
    for add_on in add_ons:
        name = add_on["name"]
        if name == "Roof Treatment":
            roof_type = add_on["type"]
            sq_ft = add_on["sq_ft"]
            rate = 0.25 if roof_type == "Asphalt" else 0.85
            min_price = 399 if roof_type == "Asphalt" else (599 if "min_599" in add_on and add_on["min_599"] else 399)
            total = max(min_price, sq_ft * rate)
            add_on_results.append((name.lower(), total))
        elif name == "Gutter Cleaning":
            linear_ft = add_on["linear_ft"]
            total = max(149, linear_ft * 0.50)
            add_on_results.append((name.lower(), total))
        elif name == "Roof Blow-Off":
            hours = add_on["hours"]
            men = add_on["men"]
            total = (hours * 149) + (hours * 42 if men == 2 else 0)
            add_on_results.append((name.lower(), total))
        elif name in ["Concrete Cleaning", "Deck/Dock Cleaning"]:
            sq_ft = add_on["sq_ft"]
            total = sq_ft * 0.15
            add_on_results.append((name.lower(), total))
        elif name == "Custom":
            total = add_on["price"]
            add_on_results.append(("custom line item", total))
    return add_on_results

def save_estimate(account_name, customer_info, inputs, results):
    estimate_data = {
        "account_name": account_name,
        "customer_info": customer_info,
        "inputs": inputs,
        "results": results,
        "timestamp": datetime.now().isoformat()
    }
    filename = os.path.join(ESTIMATES_DIR, f"{account_name.lower().replace(' ', '_')}.json")
    with open(filename, "w") as f:
        json.dump(estimate_data, f, indent=4)
    st.success(f"Estimate saved as {filename}! Please manually commit this file to GitHub to persist it.")

# Streamlit Interface
st.title("CC Inc. Pricing Calculator")

# Check if we're editing an estimate
if "edit_estimate" in st.session_state and st.session_state.edit_estimate:
    estimate_data = st.session_state.edit_estimate
    default_values = estimate_data["inputs"]
    default_customer = estimate_data["customer_info"]
else:
    default_values = {}
    default_customer = {}

# Customer Information
st.header("Customer Information")
first_name = st.text_input("First Name", value=default_customer.get("first_name", ""))
last_name = st.text_input("Last Name", value=default_customer.get("last_name", ""))
email = st.text_input("Email", value=default_customer.get("email", ""))
phone = st.text_input("Phone", value=default_customer.get("phone", ""))
address = st.text_area("Address", value=default_customer.get("address", ""))

# Estimate Inputs
st.header("Estimate Details")
account_name = st.text_input("Account Name", value=default_values.get("account_name", ""))
sq_ft = st.number_input("Square Footage", min_value=0, value=default_values.get("sq_ft", 0))
stories = st.selectbox("Number of Stories", [1, 1.5, 2, 2.5, 3], index=[1, 1.5, 2, 2.5, 3].index(default_values.get("stories", 1)))
siding = st.selectbox("Siding Type", ["Brick", "Metal", "Vinyl", "Shiplap", "Hardie/LP", "Log/Half-Log"], index=["Brick", "Metal", "Vinyl", "Shiplap", "Hardie/LP", "Log/Half-Log"].index(default_values.get("siding", "Brick")))
cleaning = st.selectbox("Cleaning Type", ["Soap/Scrub", "SH"], index=["Soap/Scrub", "SH"].index(default_values.get("cleaning", "Soap/Scrub")))
small_overhangs = st.number_input("Small Overhangs", min_value=0, value=default_values.get("small_overhangs", 0))
medium_overhangs = st.number_input("Medium Overhangs", min_value=0, value=default_values.get("medium_overhangs", 0))
large_overhangs = st.number_input("Large Overhangs", min_value=0, value=default_values.get("large_overhangs", 0))
small_decks = st.number_input("Small Decks", min_value=0, value=default_values.get("small_decks", 0))
medium_decks = st.number_input("Medium Decks", min_value=0, value=default_values.get("medium_decks", 0))
large_decks = st.number_input("Large Decks", min_value=0, value=default_values.get("large_decks", 0))
ladder_spots_hw = st.number_input("Ladder Spots (House Washing)", min_value=0, value=default_values.get("ladder_spots_hw", 0))
ladder_spots_pc = st.number_input("Ladder Spots (Pest Control)", min_value=0, value=default_values.get("ladder_spots_pc", 0))
rodent_stations = st.number_input("Rodent Stations", min_value=0, value=default_values.get("rodent_stations", 4))
rodent_interior = st.checkbox("Rodent Interior Monitoring", value=default_values.get("rodent_interior", False))
ext_standard = st.number_input("Exterior Standard Windows", min_value=0, value=default_values.get("ext_standard", 0))
ext_high = st.number_input("Exterior High Windows", min_value=0, value=default_values.get("ext_high", 0))
int_standard = st.number_input("Interior Standard Windows", min_value=0, value=default_values.get("int_standard", 0))
int_high = st.number_input("Interior High Windows", min_value=0, value=default_values.get("int_high", 0))
tracks_sills = st.number_input("Tracks/Sills Price (default 99)", min_value=0, value=default_values.get("tracks_sills", 99))

# Initialize session state
if "results" not in st.session_state:
    st.session_state.results = None
if "add_ons" not in st.session_state:
    st.session_state.add_ons = []
if "show_add_ons_form" not in st.session_state:
    st.session_state.show_add_ons_form = False
if "edit_estimate" not in st.session_state:
    st.session_state.edit_estimate = None

# Calculate
if st.button("Calculate"):
    # Validate inputs
    if not account_name:
        st.error("Please enter an Account Name.")
    else:
        # Calculate estimate
        house_washing = calculate_house_washing(sq_ft, stories, siding, cleaning, small_overhangs, medium_overhangs, large_overhangs,
                                                small_decks, medium_decks, large_decks, ladder_spots_hw)
        pest_control = calculate_pest_control(sq_ft, small_overhangs, medium_overhangs, large_overhangs,
                                              small_decks, medium_decks, large_decks, ladder_spots_pc)
        rodent_control = calculate_rodent_control(rodent_stations, rodent_interior)
        ext_windows, int_windows, tracks_sills_total = calculate_windows(ext_standard, ext_high, int_standard, int_high, tracks_sills)
        add_on_results = calculate_add_ons(st.session_state.add_ons)

        # Store results
        st.session_state.results = {
            "house_washing": house_washing,
            "pest_control": pest_control,
            "rodent_control": rodent_control,
            "ext_windows": ext_windows,
            "int_windows": int_windows,
            "tracks_sills": tracks_sills_total,
            "add_ons": add_on_results
        }
        st.session_state.show_add_ons_form = True

# Display results
if st.session_state.results:
    st.write("### Pricing Estimate")
    total = 0
    st.write(f"house washing: {st.session_state.results['house_washing']:.2f}")
    total += st.session_state.results['house_washing']
    st.write(f"pest control: {st.session_state.results['pest_control']:.2f}")
    total += st.session_state.results['pest_control']
    st.write(f"rodent control: {st.session_state.results['rodent_control']:.2f}")
    total += st.session_state.results['rodent_control']
    st.write(f"exterior windows: {st.session_state.results['ext_windows']:.2f}")
    total += st.session_state.results['ext_windows']
    st.write(f"interior windows: {st.session_state.results['int_windows']:.2f}")
    total += st.session_state.results['int_windows']
    st.write(f"tracks and sills: {st.session_state.results['tracks_sills']:.2f}")
    total += st.session_state.results['tracks_sills']
    for add_on_name, add_on_price in st.session_state.results["add_ons"]:
        st.write(f"{add_on_name}: {add_on_price:.2f}")
        total += add_on_price
    st.write(f"**Total: {total:.2f}**")

    # Save Estimate
    if st.button("Save Estimate"):
        customer_info = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "address": address
        }
        inputs = {
            "account_name": account_name,
            "sq_ft": sq_ft,
            "stories": stories,
            "siding": siding,
            "cleaning": cleaning,
            "small_overhangs": small_overhangs,
            "medium_overhangs": medium_overhangs,
            "large_overhangs": large_overhangs,
            "small_decks": small_decks,
            "medium_decks": medium_decks,
            "large_decks": large_decks,
            "ladder_spots_hw": ladder_spots_hw,
            "ladder_spots_pc": ladder_spots_pc,
            "rodent_stations": rodent_stations,
            "rodent_interior": rodent_interior,
            "ext_standard": ext_standard,
            "ext_high": ext_high,
            "int_standard": int_standard,
            "int_high": int_high,
            "tracks_sills": tracks_sills
        }
        save_estimate(account_name, customer_info, inputs, st.session_state.results)

# Add-Ons Section
if st.session_state.show_add_ons_form:
    st.write("### Would you like any additional services?")
    add_on_options = ["Roof Treatment", "Gutter Cleaning", "Roof Blow-Off", "Concrete Cleaning", "Deck/Dock Cleaning", "Custom"]
    selected_add_ons = st.multiselect("Select additional services:", add_on_options)

    add_ons = []
    for add_on in selected_add_ons:
        st.write(f"#### {add_on}")
        if add_on == "Roof Treatment":
            roof_type = st.selectbox("Roof Type", ["Asphalt", "Other"], key=f"roof_type_{add_on}")
            roof_sq_ft = st.number_input("Roof Square Footage", min_value=0, value=0, key=f"roof_sq_ft_{add_on}")
            min_599 = st.checkbox("Minimum $599 (for non-Asphalt roofs)", key=f"min_599_{add_on}")
            add_ons.append({"name": add_on, "type": roof_type, "sq_ft": roof_sq_ft, "min_599": min_599})
        elif add_on == "Gutter Cleaning":
            linear_ft = st.number_input("Linear Feet of Gutters", min_value=0, value=0, key=f"linear_ft_{add_on}")
            add_ons.append({"name": add_on, "linear_ft": linear_ft})
        elif add_on == "Roof Blow-Off":
            hours = st.number_input("Hours Required", min_value=0, value=0, key=f"hours_{add_on}")
            men = st.selectbox("Number of Men", [1, 2], key=f"men_{add_on}")
            add_ons.append({"name": add_on, "hours": hours, "men": men})
        elif add_on in ["Concrete Cleaning", "Deck/Dock Cleaning"]:
            add_on_sq_ft = st.number_input("Square Footage", min_value=0, value=0, key=f"sq_ft_{add_on}")
            add_ons.append({"name": add_on, "sq_ft": add_on_sq_ft})
        elif add_on == "Custom":
            custom_price = st.number_input("Custom Price", min_value=0.0, value=0.0, key=f"price_{add_on}")
            add_ons.append({"name": add_on, "price": custom_price})

    if st.button("Add Selected Services and Recalculate"):
        st.session_state.add_ons = add_ons
        house_washing = calculate_house_washing(sq_ft, stories, siding, cleaning, small_overhangs, medium_overhangs, large_overhangs,
                                                small_decks, medium_decks, large_decks, ladder_spots_hw)
        pest_control = calculate_pest_control(sq_ft, small_overhangs, medium_overhangs, large_overhangs,
                                              small_decks, medium_decks, large_decks, ladder_spots_pc)
        rodent_control = calculate_rodent_control(rodent_stations, rodent_interior)
        ext_windows, int_windows, tracks_sills_total = calculate_windows(ext_standard, ext_high, int_standard, int_high, tracks_sills)
        add_on_results = calculate_add_ons(st.session_state.add_ons)

        st.session_state.results = {
            "house_washing": house_washing,
            "pest_control": pest_control,
            "rodent_control": rodent_control,
            "ext_windows": ext_windows,
            "int_windows": int_windows,
            "tracks_sills": tracks_sills_total,
            "add_ons": add_on_results
        }
        st.rerun()

# Clear edit state after saving
if st.session_state.edit_estimate and st.session_state.results:
    st.session_state.edit_estimate = None
