import streamlit as st
import pandas as pd
import time
from fpdf import FPDF
import yagmail

# Initialize session state
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0
if 'running' not in st.session_state:
    st.session_state.running = False
if 'results' not in st.session_state:
    st.session_state.results = []
if 'medals' not in st.session_state:
    st.session_state.medals = {'Red': 0, 'Blue': 0, 'Green': 0, 'Yellow': 0}

st.title("🏅 Athletic Event Stopwatch")

# Display GIF
st.image("https://www.ryukyulife.com/wp-content/uploads/2017/09/sportsday.gif", caption="School Athletics in Action", use_container_width=True)

# Stopwatch Controls
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ Start"):
        st.session_state.start_time = time.time() - st.session_state.elapsed_time
        st.session_state.running = True
with col2:
    if st.button("⏸️ Stop"):
        st.session_state.elapsed_time = time.time() - st.session_state.start_time
        st.session_state.running = False
with col3:
    if st.button("🔄 Reset"):
        st.session_state.start_time = None
        st.session_state.elapsed_time = 0
        st.session_state.running = False

# Display Timer
if st.session_state.running:
    st.session_state.elapsed_time = time.time() - st.session_state.start_time
st.metric("⏱️ Elapsed Time", f"{st.session_state.elapsed_time:.2f} seconds")

# Record Result
name = st.text_input("Participant Name")
house = st.selectbox("House", ["Red", "Blue", "Green", "Yellow"])
if st.button("✅ Record Time"):
    st.session_state.results.append({
        "Name": name,
        "House": house,
        "Time": round(st.session_state.elapsed_time, 2)
    })
    st.success(f"Recorded {name} from {house} house with time {round(st.session_state.elapsed_time, 2)}s")

# Medal Count
st.subheader("🏆 Medal Tally")
medal_house = st.selectbox("Award Medal to", ["Red", "Blue", "Green", "Yellow"])
if st.button("🥇 Add Medal"):
    st.session_state.medals[medal_house] += 1
st.write(pd.DataFrame.from_dict(st.session_state.medals, orient='index', columns=['Medals']))

# Results Table
st.subheader("📋 Event Results")
df = pd.DataFrame(st.session_state.results)
st.dataframe(df)

# Export Options
def export_csv():
    df.to_csv("event_results.csv", index=False)
    st.success("CSV exported!")

def export_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Athletic Event Results", ln=True, align='C')
    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Name']} - {row['House']} - {row['Time']}s", ln=True)
    pdf.output("event_results.pdf")
    st.success("PDF exported!")

col4, col5 = st.columns(2)
with col4:
    if st.button("📤 Export CSV"):
        export_csv()
with col5:
    if st.button("📝 Export PDF"):
        export_pdf()

# Email Option
st.subheader("📧 Email Results")
recipient = st.text_input("Recipient Email")
if st.button("Send Email"):
    try:
        yag = yagmail.SMTP("your_email@gmail.com", "your_app_password")
        yag.send(
            to=recipient,
            subject="Athletic Event Results",
            contents="Attached are the results of the athletic event.",
            attachments=["event_results.csv", "event_results.pdf"]
        )
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")