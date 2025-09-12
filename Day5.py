import streamlit as st

st.title("🔄 Universal Unit Converter")

category = st.selectbox("Choose conversion type", ["Currency", "Temperature", "Length", "Weight"])

value = st.number_input("Enter value", value=0.0)

if category == "Currency":
    from_currency = st.selectbox("From", ["USD", "INR", "EUR"])
    to_currency = st.selectbox("To", ["USD", "INR", "EUR"])
    # Placeholder rates (you can integrate with an API like exchangerate-api)
    rates = {"USD": 1, "INR": 83, "EUR": 0.93}
    result = value / rates[from_currency] * rates[to_currency]
    st.metric(label=f"{from_currency} → {to_currency}", value=f"{result:.2f} {to_currency}")

elif category == "Temperature":
    from_temp = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
    to_temp = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])
    def convert_temp(val, from_t, to_t):
        if from_t == to_t:
            return val
        if from_t == "Celsius":
            if to_t == "Fahrenheit": return val * 9/5 + 32
            if to_t == "Kelvin": return val + 273.15
        if from_t == "Fahrenheit":
            if to_t == "Celsius": return (val - 32) * 5/9
            if to_t == "Kelvin": return (val - 32) * 5/9 + 273.15
        if from_t == "Kelvin":
            if to_t == "Celsius": return val - 273.15
            if to_t == "Fahrenheit": return (val - 273.15) * 9/5 + 32
    result = convert_temp(value, from_temp, to_temp)
    st.metric(label=f"{from_temp} → {to_temp}", value=f"{result:.2f} {to_temp}")

elif category == "Length":
    from_len = st.selectbox("From", ["Meters", "Kilometers", "Miles", "Feet"])
    to_len = st.selectbox("To", ["Meters", "Kilometers", "Miles", "Feet"])
    factors = {"Meters": 1, "Kilometers": 1000, "Miles": 1609.34, "Feet": 0.3048}
    result = value * factors[from_len] / factors[to_len]
    st.metric(label=f"{from_len} → {to_len}", value=f"{result:.2f} {to_len}")

elif category == "Weight":
    from_wt = st.selectbox("From", ["Kilograms", "Grams", "Pounds", "Ounces"])
    to_wt = st.selectbox("To", ["Kilograms", "Grams", "Pounds", "Ounces"])
    factors = {"Kilograms": 1, "Grams": 0.001, "Pounds": 0.453592, "Ounces": 0.0283495}
    result = value * factors[from_wt] / factors[to_wt]
    st.metric(label=f"{from_wt} → {to_wt}", value=f"{result:.2f} {to_wt}")