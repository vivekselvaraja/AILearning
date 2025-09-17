import streamlit as st
from lxml import html
import pandas as pd
import re
from datetime import timedelta

# -----------------------------
# App Title & Instructions
# -----------------------------
st.title("📘 Social Eagle Course Topic, Duration & Status Extractor for each Week")
st.write("Upload an HTML file and extract topic names, durations, and status. Rows with missing titles will be skipped. Status is color-coded. Total duration and incomplete topics are summarized.")

# -----------------------------
# File Upload & XPath Inputs
# -----------------------------
uploaded_file = st.file_uploader("📤 Upload HTML File", type=["html", "htm"])
xpath_topic = st.text_input("🧠 XPath for Topics", value="//div[contains(@class, 'lecture-title')]/text()")
xpath_duration = st.text_input("⏱️ XPath for Durations", value="//span[contains(@class, 'duration')]/text()")
xpath_status = st.text_input("📌 XPath for Status (class attribute)", value="//div[contains(@class, 'status-icon')]/@class")

# -----------------------------
# Helper: Convert HH:MM:SS to seconds
# -----------------------------
def duration_to_seconds(duration_str):
    try:
        h, m, s = map(int, re.findall(r"\d+", duration_str))
        return h * 3600 + m * 60 + s
    except:
        return 0

# -----------------------------
# Extraction Logic
# -----------------------------
def extract_from_html(html_content, topic_xpath, duration_xpath, status_xpath):
    try:
        tree = html.fromstring(html_content)

        topics = tree.xpath(topic_xpath)
        durations = tree.xpath(duration_xpath)
        statuses_raw = tree.xpath(status_xpath)

        topics = [str(t).strip() for t in topics]
        durations = [str(d).strip() for d in durations]
        statuses = [
            "Completed" if "completed" in s else
            "In Progress" if "in-progress" in s else
            "Not Started" for s in statuses_raw
        ]

        rows = []
        for i in range(max(len(topics), len(durations), len(statuses))):
            topic = topics[i] if i < len(topics) else ""
            duration = durations[i] if i < len(durations) else ""
            status = statuses[i] if i < len(statuses) else ""
            if topic:
                rows.append({"Topic": topic, "Duration": duration, "Status": status})

        return pd.DataFrame(rows)

    except Exception as e:
        st.error(f"❌ Error during extraction: {e}")
        return pd.DataFrame()

# -----------------------------
# Trigger Extraction
# -----------------------------
if uploaded_file and xpath_topic and xpath_duration and xpath_status:
    html_content = uploaded_file.read()
    df = extract_from_html(html_content, xpath_topic, xpath_duration, xpath_status)

    if not df.empty:
        st.subheader("📊 Extracted Data")

        # Apply color styling
        def highlight_status(val):
            if val == "Completed":
                return "background-color: #d4edda; color: green"
            else:
                return "background-color: #f8d7da; color: red"

        styled_df = df.style.applymap(highlight_status, subset=["Status"])
        st.dataframe(styled_df, use_container_width=True)

        # -----------------------------
        # Total Duration Calculation
        # -----------------------------
        total_seconds = sum(duration_to_seconds(d) for d in df["Duration"])
        total_time = str(timedelta(seconds=total_seconds))
        st.subheader("⏳ Total Duration")
        st.write(f"**{total_time}** (HH:MM:SS)")

        # -----------------------------
        # List of Incomplete Topics
        # -----------------------------
        incomplete_topics = df[df["Status"] != "Completed"]["Topic"].tolist()
        if incomplete_topics:
            st.subheader("❗ Topics Not Completed")
            for topic in incomplete_topics:
                st.markdown(f"- {topic}")
        else:
            st.subheader("✅ All topics are marked as completed!")

        st.success(f"✅ Extracted {len(df)} rows with valid titles.")
    else:
        st.warning("No valid rows extracted. Check your XPath expressions or file content.")