import streamlit as st
import random
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()
EMAIL_USER = os.getenv("GMAIL_EMAIL")
EMAIL_PASS = os.getenv("GMAIL_EMAIL_PASSWORD")

# --- Music Tracks ---
MUSIC_TRACKS = [
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
]

# --- Constants ---
CHOICES = ["Rock 🪨", "Paper 📄", "Scissors ✂️"]
WIN_MAP = {
    "Rock 🪨": "Scissors ✂️",
    "Paper 📄": "Rock 🪨",
    "Scissors ✂️": "Paper 📄"
}
WIN_GIF = "https://media.giphy.com/media/111ebonMs90YLu/giphy.gif"
LOSE_GIF = "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"
DRAW_GIF = "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif"

# --- Background Styling ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1607083206173-3e3b5b8e0f3c");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #fff;
    }
    .stButton > button {
        background-color: #FF4500 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        font-size: 18px;
        border: none;
        box-shadow: 2px 2px 5px #00000050;
    }
    .stButton > button:hover {
        background-color: #FF6347 !important;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State ---
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "history" not in st.session_state:
    st.session_state.history = []

# --- Title ---
st.markdown("<h1 style='text-align:center; color:#FFD700;'>🎮 Rock, Paper, Scissors</h1>", unsafe_allow_html=True)

# --- Sidebar: User Info ---
st.sidebar.header("🧑 Your Info")
user_name = st.sidebar.text_input("Name")
user_email = st.sidebar.text_input("Email")
send_email = st.sidebar.button("📤 Send Score Summary")

# --- Game Play ---
st.markdown("<h3 style='color:#00FF00;'>Choose your move:</h3>", unsafe_allow_html=True)
user_choice = st.radio("Your Choice", CHOICES, horizontal=True)
play_clicked = st.button("▶️ Play")

if play_clicked:
    computer_choice = random.choice(CHOICES)
    result = ""
    selected_track = random.choice(MUSIC_TRACKS)

    if user_choice == computer_choice:
        result = "It's a draw!"
        st.image(DRAW_GIF, caption="Draw!", use_container_width=True)
    elif WIN_MAP[user_choice] == computer_choice:
        result = "You win!"
        st.session_state.user_score += 1
        st.image(WIN_GIF, caption="Victory!", use_container_width=True)
    else:
        result = "Computer wins!"
        st.session_state.computer_score += 1
        st.image(LOSE_GIF, caption="Defeat!", use_container_width=True)

    st.session_state.history.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "User": user_choice,
        "Computer": computer_choice,
        "Result": result
    })

    st.success(f"Computer chose: {computer_choice}")
    st.info(result)

    # --- Autoplay Music After Game ---
    st.markdown(f"""
        <audio autoplay>
            <source src="{selected_track}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

# --- Scoreboard ---
st.markdown("---")
st.header("📊 Scoreboard")
st.write(f"**{user_name or 'You'}:** {st.session_state.user_score}")
st.write(f"**Computer:** {st.session_state.computer_score}")

# --- History ---
st.markdown("---")
st.header("🕵️ Game History")
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history))
else:
    st.info("No games played yet.")

# --- Email Function ---
def send_score_email(to_email, user_name, user_score, computer_score, history):
    sender_email = EMAIL_USER
    app_password = EMAIL_PASS
    selected_track = random.choice(MUSIC_TRACKS)

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Rock, Paper, Scissors Score Summary"
    message["From"] = sender_email
    message["To"] = to_email

    body = f"""
Hi {user_name},

Here's your game summary:

🧑 You: {user_score}
🤖 Computer: {computer_score}
🎮 Games Played: {len(history)}
🕵️ Last Result: {history[-1]['Result'] if history else 'N/A'}

🎵 Here's a track to celebrate or reflect:
{selected_track}

Thanks for playing!
    """

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_email, message.as_string())
        return True, selected_track
    except Exception as e:
        st.error(f"Email failed: {e}")
        return False, None

# --- Send Email ---
if send_email:
    if user_email and user_name:
        success, music_after_email = send_score_email(
            user_email, user_name,
            st.session_state.user_score,
            st.session_state.computer_score,
            st.session_state.history
        )
        if success:
            st.success(f"Score summary sent to {user_email}")
            # --- Autoplay Music After Email ---
            st.markdown(f"""
                <audio autoplay>
                    <source src="{music_after_email}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)
    else:
        st.error("Please enter both name and email.")