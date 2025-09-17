import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- DB Setup ---
conn = sqlite3.connect("gym_log.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS workouts (
    date TEXT, exercise TEXT, sets INTEGER, reps INTEGER, weight REAL
)''')
conn.commit()

# --- Common Exercises ---
common_exercises = [
    "Bench Press", "Squat", "Deadlift", "Overhead Press", "Barbell Row",
    "Pull-Up", "Push-Up", "Dumbbell Curl", "Tricep Extension", "Leg Press",
    "Lunges", "Plank", "Lat Pulldown", "Cable Fly", "Shoulder Shrug"
]

# --- Input Form ---
with st.form("log_form"):
    exercise = st.selectbox("Exercise", options=common_exercises)
    sets = st.number_input("Sets", min_value=1, step=1)
    reps = st.number_input("Reps", min_value=1, step=1)
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.5)
    submitted = st.form_submit_button("Log Workout")
    if submitted:
        c.execute("INSERT INTO workouts VALUES (?, ?, ?, ?, ?)",
                  (datetime.today().strftime('%Y-%m-%d'), exercise, sets, reps, weight))
        conn.commit()
        st.success("Workout logged!")

# --- History Table ---
st.subheader("📋 Workout History")
df = pd.read_sql_query("SELECT * FROM workouts", conn)
st.dataframe(df)

# --- Weekly Progress Graph ---
st.subheader("📈 Weekly Progress")
if not df.empty:
    df['volume'] = df['sets'] * df['reps'] * df['weight']
    df['week'] = pd.to_datetime(df['date']).dt.to_period('W').astype(str)
    weekly = df.groupby('week')['volume'].sum().reset_index()
    st.bar_chart(weekly.set_index('week'))
else:
    st.info("No data yet. Log a workout to see progress.")