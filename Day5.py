import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# App layout
st.set_page_config(page_title="Unit Converter", layout="wide")
st.title("🔄 Universal Unit Converter")

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Conversion type and input
category = st.selectbox("Choose conversion type", ["Currency", "Temperature", "Length", "Weight"])
value = st.number_input("Enter value", min_value=0.0, value=1.0)

# Helper to prevent same unit selection
def filtered_select(label, options, exclude):
    return st.selectbox(label, [opt for opt in options if opt != exclude])

# Layout: Left for input, Right for result
left, right = st.columns(2)

with left:
    if category == "Currency":
        currencies = ["USD", "INR", "EUR", "GBP", "JPY"]
        from_curr = st.selectbox("From Currency", currencies)
        to_curr = filtered_select("To Currency", currencies, from_curr)

        url = f"https://api.apilayer.com/exchangerates_data/latest?base={from_curr}&symbols={to_curr}"
        headers = {"apikey": api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "rates" in data and to_curr in data["rates"]:
                rate = data["rates"][to_curr]
                converted = value * rate
                result_text = f"{value} {from_curr} → {converted:.2f} {to_curr}"
                st.session_state.history.append(result_text)

                with right:
                    st.metric(label=f"{from_curr} → {to_curr}", value=f"{converted:.2f} {to_curr}")
            else:
                st.error(f"No rate found for {to_curr}. Full response: {data}")
        except Exception as e:
            st.error(f"Currency conversion failed: {e}")

    elif category == "Temperature":
        units = ["Celsius", "Fahrenheit", "Kelvin"]
        from_temp = st.selectbox("From", units)
        to_temp = filtered_select("To", units, from_temp)

        def convert_temp(val, from_u, to_u):
            if from_u == "Celsius":
                return val * 9/5 + 32 if to_u == "Fahrenheit" else val + 273.15
            if from_u == "Fahrenheit":
                return (val - 32) * 5/9 if to_u == "Celsius" else (val - 32) * 5/9 + 273.15
            if from_u == "Kelvin":
                return val - 273.15 if to_u == "Celsius" else (val - 273.15) * 9/5 + 32

        result = convert_temp(value, from_temp, to_temp)
        result_text = f"{value} {from_temp} → {result:.2f} {to_temp}"
        st.session_state.history.append(result_text)

        with right:
            st.metric(label=f"{from_temp} → {to_temp}", value=f"{result:.2f} {to_temp}")

    elif category == "Length":
        units = {"Meters": 1, "Kilometers": 1000, "Miles": 1609.34, "Feet": 0.3048}
        from_len = st.selectbox("From", list(units.keys()))
        to_len = filtered_select("To", list(units.keys()), from_len)
        result = value * units[from_len] / units[to_len]
        result_text = f"{value} {from_len} → {result:.2f} {to_len}"
        st.session_state.history.append(result_text)

        with right:
            st.metric(label=f"{from_len} → {to_len}", value=f"{result:.2f} {to_len}")

    elif category == "Weight":
        units = {"Kilograms": 1, "Grams": 0.001, "Pounds": 0.453592, "Ounces": 0.0283495}
        from_wt = st.selectbox("From", list(units.keys()))
        to_wt = filtered_select("To", list(units.keys()), from_wt)
        result = value * units[from_wt] / units[to_wt]
        result_text = f"{value} {from_wt} → {result:.2f} {to_wt}"
        st.session_state.history.append(result_text)

        with right:
            st.metric(label=f"{from_wt} → {to_wt}", value=f"{result:.2f} {to_wt}")

# 📜 Show conversion history
st.subheader("🕘 Conversion History")
for entry in reversed(st.session_state.history[-10:]):
    st.write(entry)
