import streamlit as st
import pandas as pd
import os
from datetime import date

# --- CONFIGURATION ---
ORGANIZER_USER = "admin"
ORGANIZER_PASS = "password123"
CSV_FILE = "registrations.csv"

# --- INITIALIZE SESSION STATE ---
if "registrations" not in st.session_state:
    if os.path.exists(CSV_FILE):
        st.session_state.registrations = pd.read_csv(CSV_FILE).to_dict("records")
    else:
        st.session_state.registrations = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- HEADER MODE SELECTION ---
mode = st.radio("Select Mode", ["Visitor", "Organizer"], horizontal=True)


# --- ORGANIZER MODE ---
if mode == "Organizer":
    st.title("Organizer Login")
    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Log In"):
            if username == ORGANIZER_USER and password == ORGANIZER_PASS:
                st.session_state.logged_in = True
                st.rerun()  # Rerun to refresh the page after login
            else:
                st.error("Invalid credentials")
    else:
        # Display dashboard when logged in
        st.title("📋 Registration Dashboard")
        df = pd.DataFrame(st.session_state.registrations)
        st.markdown(f"**Total Registrations:** {len(df)}")
        st.dataframe(df)
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv_bytes,
            file_name=CSV_FILE,
            mime="text/csv"
        )

        # Admin cancellation
        cancel_email = st.text_input("Enter email to cancel as an Admin")
        if cancel_email:
            df = pd.DataFrame(st.session_state.registrations)
            matches = df[df["Email"] == cancel_email]

            if matches.empty:
                st.warning("No registrations found for this email.")
            else:
                cancel_choice = st.selectbox(
                    "Select a registration to cancel",
                    matches.apply(lambda row: f"{row['Event']} on {row['Date']} at {row['Time Slot']}", axis=1)
                )
                if st.button("Confirm Cancellation"):
                    # Identify index to remove
                    idx_to_remove = matches.index[matches.apply(
                        lambda row: f"{row['Event']} on {row['Date']} at {row['Time Slot']}" == cancel_choice,
                        axis=1
                    )][0]

                    # Remove from session_state
                    del st.session_state.registrations[idx_to_remove]

                    # Rewrite CSV
                    updated_df = pd.DataFrame(st.session_state.registrations)
                    updated_df.to_csv(CSV_FILE, index=False)

                    st.success("Registration cancelled successfully!")
                    st.rerun()

        # Logout button
        if st.sidebar.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

# --- VISITOR MODE ---
else:
    # Allowed date range
    start_date = date(2025, 9, 22)
    end_date = date(2025, 9, 26)
    MAX_CAPACITY = 24

    # All time slots with boundaries
    slot_options = {
        "08:00–10:00": (8, 10),
        "10:00–12:00": (10, 12),
        "12:00–14:00": (12, 14),
        "14:00–16:00": (14, 16),
        "16:00–18:00": (16, 18)
    }

    st.title("🎟️ Event Registration")

    # Event selection outside form for dynamic filtering
    event_choice = st.selectbox(
        "Event Choice",
        ["Keynote", "Workshop A", "Workshop B", "Networking"]
    )

    # Filter slots based on event logic
    if event_choice == "Keynote":
        valid_slots = [slot for slot, (start, end) in slot_options.items() if end <= 10]
    elif event_choice == "Networking":
        valid_slots = [slot for slot, (start, end) in slot_options.items() if start >= 16]
    else:
        valid_slots = list(slot_options.keys())

    # Date selection
    reg_date = st.date_input("Date", min_value=start_date, max_value=end_date)

    # Slot selection
    slot = st.selectbox("Time Slot", valid_slots)

    # Count current registrations for selected event/date/slot
    df = pd.DataFrame(st.session_state.registrations)
    filtered = df[
        (df["Event"] == event_choice) &
        (df["Date"] == reg_date.isoformat()) &
        (df["Time Slot"] == slot)
    ]
    current_count = len(filtered)
    remaining = MAX_CAPACITY - current_count

    # Show availability
    if remaining > 0:
        st.success(f"✅ {remaining} spots left for {event_choice} on {reg_date} at {slot}")
    else:
        st.error(f"❌ Slot FULL for {event_choice} on {reg_date} at {slot}")

    # Registration form
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Name", max_chars=50)
        email = st.text_input("Email", placeholder="you@example.com")
        submitted = st.form_submit_button("Register")

        if submitted:
            if not name or not email:
                st.error("Name and Email are required.")
            elif remaining <= 0:
                st.error("This slot is full. Please choose another.")
            else:
                entry = {
                    "Name": name,
                    "Email": email,
                    "Event": event_choice,
                    "Date": reg_date.isoformat(),
                    "Time Slot": slot
                }
                st.session_state.registrations.append(entry)

                df_new = pd.DataFrame([entry])
                if os.path.exists(CSV_FILE):
                    df_new.to_csv(CSV_FILE, mode="a", header=False, index=False)
                else:
                    df_new.to_csv(CSV_FILE, mode="w", header=True, index=False)

                st.success("Registration successful!")
                st.rerun()

    # Live total count
    total = len(st.session_state.registrations)
    st.info(f"🎉 Total registrations so far: **{total}**")
    st.markdown("---")
    st.subheader("❌ Cancel Your Registration")

    cancel_email = st.text_input("Enter your registered email to cancel")
    if cancel_email:
        df = pd.DataFrame(st.session_state.registrations)
        matches = df[df["Email"] == cancel_email]

        if matches.empty:
            st.warning("No registrations found for this email.")
        else:
            cancel_choice = st.selectbox(
                "Select a registration to cancel",
                matches.apply(lambda row: f"{row['Event']} on {row['Date']} at {row['Time Slot']}", axis=1)
            )
            if st.button("Confirm Cancellation"):
                # Identify index to remove
                idx_to_remove = matches.index[matches.apply(
                    lambda row: f"{row['Event']} on {row['Date']} at {row['Time Slot']}" == cancel_choice,
                    axis=1
                )][0]

                # Remove from session_state
                del st.session_state.registrations[idx_to_remove]

                # Rewrite CSV
                updated_df = pd.DataFrame(st.session_state.registrations)
                updated_df.to_csv(CSV_FILE, index=False)

                st.success("Registration cancelled successfully!")
                st.rerun()
