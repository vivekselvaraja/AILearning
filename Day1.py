import streamlit as st

# Title
st.title("Assignment Day 1 Greeting App by Vivek")

# Input fields
name = st.text_input("Enter your First Name")
age = st.slider("Select your Age", 1, 100, 25)

# Button to submit
if st.button("Greet Me"):
    if name:
        st.success(f"Hello {name}! You are {age} years old 🎉")
    else:
        st.warning("Please enter your Name.")