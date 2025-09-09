# Scenario:
# Friends go out for dinner/trip and want to split expenses fairly.

# Task:

# User enters: total amount + number of people.

# Optionally, add each person’s name & contribution.

# App calculates how much each person should pay or get back.
import streamlit as st
import pandas as pd

st.title("💸 Fair Expense Splitter")

# Session state to reset inputs
if "reset" not in st.session_state:
    st.session_state.reset = False

def clear_inputs():
    st.session_state.reset = True

# Inputs
if st.session_state.reset:
    total_amount = 0.0
    num_people = 1
    st.session_state.reset = False
else:
    total_amount = st.number_input("Enter total amount spent", min_value=0.0, format="%.2f")
    num_people = st.number_input("Number of people", min_value=1, step=1)

st.subheader("Optional: Enter individual contributions")
names = []
contributions = []

for i in range(int(num_people)):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"Person {i+1} Name", key=f"name_{i}")
    with col2:
        contribution = st.number_input(f"{name or 'Person'}'s Contribution", min_value=0.0, format="%.2f", key=f"contrib_{i}")
    names.append(name if name else f"Person {i+1}")
    contributions.append(contribution)

# Calculate button
if st.button("Calculate Settlement"):
    fair_share = total_amount / num_people
    balances = [round(p - fair_share, 2) for p in contributions]

    df = pd.DataFrame({
        "Name": names,
        "Paid": contributions,
        "Balance to Pay(-) and Get(+)": balances
    })

    st.subheader("💰 Settlement Summary")
    st.dataframe(df)

    # Bar chart
    st.subheader("📊 Balance Chart")
    st.bar_chart(df.set_index("Name")["Balance to Pay(-) and Get(+)"])

    # Settle up logic
    st.subheader("🔄 Settle Up Suggestions")
    debtors = df[df["Balance to Pay(-) and Get(+)"] < 0].copy()
    creditors = df[df["Balance to Pay(-) and Get(+)"] > 0].copy()

    debtors["Balance to Pay(-) and Get(+)"] = debtors["Balance to Pay(-) and Get(+)"].abs()
    for i, debtor in debtors.iterrows():
        for j, creditor in creditors.iterrows():
            if debtor["Balance to Pay(-) and Get(+)"] == 0:
                break
            if creditor["Balance to Pay(-) and Get(+)"] == 0:
                continue
            amount = min(debtor["Balance to Pay(-) and Get(+)"], creditor["Balance to Pay(-) and Get(+)"])
            st.write(f"{debtor['Name']} pays ₹{amount} to {creditor['Name']}")
            debtor["Balance to Pay(-) and Get(+)"] -= amount
            creditors.at[j, "Balance to Pay(-) and Get(+)"] -= amount

    # Export CSV
    st.subheader("📁 Export Results")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="expense_split.csv", mime="text/csv")

# Clear button
st.button("🧹 Clear All", on_click=clear_inputs)