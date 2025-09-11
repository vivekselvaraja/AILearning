import streamlit as st

st.title("Simple Calculator with 2 numbers")

# Input fields
num1 = st.number_input("Enter first number", value=0.0)
num2 = st.number_input("Enter second number", value=0.0)

st.write("### Choose Operation")

# Button layout
col1, col2, col3, col4 = st.columns(4)
col5, col6, col7 = st.columns(3)

result = None
operation_used = ""

with col1:
    if st.button("➕"):
        result = num1 + num2
        operation_used = "Addition"
with col2:
    if st.button("➖"):
        result = num1 - num2
        operation_used = "Subtraction"
with col3:
    if st.button("✖"):
        result = num1 * num2
        operation_used = "Multiplication"
with col4:
    if st.button("➗"):
        if num2 != 0:
            result = num1 / num2
            operation_used = "Division"
        else:
            result = "Error: Division by zero"
            operation_used = "Division"
with col5:
    if st.button("%"):
        if num2 != 0:
            result = num1 % num2
            operation_used = "Modulus"
        else:
            result = "Error: Modulo by zero"
            operation_used = "Modulus"
with col6:
    if st.button("^"):
        result = num1 ** num2
        operation_used = "Exponentiation"
with col7:
    if st.button("//"):
        if num2 != 0:
            result = num1 // num2
            operation_used = "Floor Division"
        else:
            result = "Error: Floor division by zero"
            operation_used = "Floor Division"

# Display result with operation label
if result is not None:
    st.success(f"{operation_used} Result: {result}")