import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# --- Simulated Date State ---
if "current_date" not in st.session_state:
    st.session_state.current_date = datetime.now().date()

def advance_day():
    st.session_state.current_date += timedelta(days=1)

# --- DB Setup ---
conn = sqlite3.connect("water_tracker.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS intake (
        date TEXT,
        amount REAL
    )
""")
conn.commit()

# --- Helper Functions ---
def log_intake(amount_ml):
    amount_l = amount_ml / 1000.0
    date_str = st.session_state.current_date.strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO intake (date, amount) VALUES (?, ?)", (date_str, amount_l))
    conn.commit()

def get_today_total():
    date_str = st.session_state.current_date.strftime("%Y-%m-%d")
    cursor.execute("SELECT SUM(amount) FROM intake WHERE date = ?", (date_str,))
    result = cursor.fetchone()[0]
    return result if result else 0

def clear_today_entries():
    date_str = st.session_state.current_date.strftime("%Y-%m-%d")
    cursor.execute("DELETE FROM intake WHERE date = ?", (date_str,))
    conn.commit()

def get_weekly_data():
    start_date = st.session_state.current_date - timedelta(days=6)
    start_str = start_date.strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT date, SUM(amount) as total
        FROM intake
        WHERE date >= ?
        GROUP BY date
        ORDER BY date ASC
    """, (start_str,))
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["Date", "Total"])
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%d %b")
    return df

# --- UI ---
st.set_page_config(page_title="Hydration Tracker", layout="centered")
st.title("💧 Water Intake Tracker")

daily_goal = 3.0  # Liters

# --- Date Control ---
st.subheader("🗓️ Date Control")
st.write(f"Current Date: {st.session_state.current_date.strftime('%A, %d %B %Y')}")

col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("⬅️ Previous Day"):
        st.session_state.current_date -= timedelta(days=1)
        st.rerun()
with col_next:
    if st.button("Next Day ➡️"):
        advance_day()
        st.rerun()

# Quick Add Buttons
st.subheader("Quick Add")
col1, col2, col3, col4, col5 = st.columns(5)
for vol, col in zip([100, 200, 300, 400, 500], [col1, col2, col3, col4, col5]):
    if col.button(f"{vol} ml"):
        log_intake(vol)
        st.success(f"Logged {vol}ml!")

# Custom Entry
st.subheader("Custom Entry")
custom_ml = st.number_input("Enter custom amount (ml)", min_value=50, step=50)
if st.button("Log Custom Intake"):
    log_intake(custom_ml)
    st.success(f"Logged {custom_ml}ml!")

# Clear Entries
st.subheader("🧹 Manage Entries")
if st.button("Clear Today's Entries"):
    clear_today_entries()
    st.warning("Today's entries have been cleared.")
    st.rerun()

# Progress
today_total = get_today_total()
progress = min(today_total / daily_goal, 1.0)
st.metric("Today's Total", f"{today_total:.2f}L")
st.progress(progress)

# Bottle Fill UI
fill_height = int(progress * 100)
bottle_css = f"""
<style>
.bottle {{
    width: 100px;
    height: 200px;
    border: 4px solid #555;
    border-radius: 20px;
    position: relative;
    background-color: #e0f7fa;
    margin: auto;
}}
.fill {{
    position: absolute;
    bottom: 0;
    width: 100%;
    height: {fill_height}%;
    background-color: #00bcd4;
    border-radius: 0 0 16px 16px;
    transition: height 0.5s ease;
}}
</style>
<div class="bottle">
    <div class="fill"></div>
</div>
"""
st.markdown(bottle_css, unsafe_allow_html=True)

# Feedback
if today_total < daily_goal * 0.5:
    st.info("Keep sipping! 💦")
elif today_total < daily_goal * 0.9:
    st.warning("Almost there! 🚰")
else:
    st.success("Hydrated hero! 🟢")

# Weekly Chart
st.subheader("📊 Weekly Hydration")
weekly_df = get_weekly_data()
if not weekly_df.empty:
    st.bar_chart(weekly_df.set_index("Date"))
else:
    st.write("No data yet. Start logging your intake!")

