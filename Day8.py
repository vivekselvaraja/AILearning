import streamlit as st

# === Static Exchange Rates ===
rates = {
    "INR": 1.0,
    "USD": 83.0,     # 1 USD = 83 INR
    "EUR": 89.0,     # 1 EUR = 89 INR
    "GBP": 103.0,    # 1 GBP = 103 INR
    "JPY": 0.56,     # 1 JPY = 0.56 INR
}

# === UI ===
st.title("💱 Currency Converter")

amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
from_currency = st.selectbox("From", list(rates.keys()))
to_currency = st.selectbox("To", list(rates.keys()))

# === Conversion Logic ===
if st.button("Convert"):
    try:
        inr_value = amount * rates[from_currency]
        converted = inr_value / rates[to_currency]
        st.success(f"{amount:.2f} {from_currency} = {converted:.2f} {to_currency}")
    except Exception as e:
        st.error(f"Conversion failed: {e}")