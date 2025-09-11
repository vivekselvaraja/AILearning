import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="wide")

# --- Session State for History ---
if "bmi_history" not in st.session_state:
    st.session_state.bmi_history = []

# --- Sidebar: History + Vertical Range ---
with st.sidebar:
    st.markdown("## 🚀 Your Health Journey")
    st.write("Each entry is a step forward. Track your progress, celebrate your wins, and keep moving toward your goals!")

    if st.session_state.bmi_history:
        history_df = pd.DataFrame(
            st.session_state.bmi_history,
            columns=["Name", "Age", "Height (cm)", "Weight (kg)", "BMI", "Category"]
        )
        st.dataframe(history_df, use_container_width=True)
        st.markdown("### 📊 BMI Trend")
        st.bar_chart(history_df["BMI"])
    else:
        st.info("No BMI records yet. Calculate to begin tracking.")

    # --- Vertical BMI Range Bar ---
    st.markdown("### 📍 BMI Range Indicator")
    def render_range_bar(bmi_val):
        bar = ""
        for i in range(35, 9, -1):
            if i == int(bmi_val):
                bar += f"<div style='background-color:#4B8BBE;color:white;padding:2px;'>⬅️ {i}</div>"
            elif i < 18.5:
                bar += f"<div style='background-color:#FFD1DC;padding:2px;'>{i}</div>"
            elif i < 25:
                bar += f"<div style='background-color:#C1F0C1;padding:2px;'>{i}</div>"
            else:
                bar += f"<div style='background-color:#FFDD99;padding:2px;'>{i}</div>"
        return bar

    if st.session_state.bmi_history:
        latest_bmi = st.session_state.bmi_history[-1][4]
        st.markdown(render_range_bar(latest_bmi), unsafe_allow_html=True)

# --- Main Title ---
st.markdown("<h2 style='text-align: center; color: #4B8BBE;'>Let's Check Your BMI and Power Up Your Health! ⚡</h2>", unsafe_allow_html=True)
st.write("You're just a few clicks away from discovering your BMI and unlocking personalized health tips. Let’s fuel your journey toward a stronger, healthier you!")

# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Your Name")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
with col2:
    height = st.number_input("Height (cm)", min_value=0.0, format="%.2f")
    weight = st.number_input("Weight (kg)", min_value=0.0, format="%.2f")

# --- BMI Logic ---
def calculate_bmi(h_cm, w_kg):
    h_m = h_cm / 100
    if h_m <= 0:
        return None
    return round(w_kg / (h_m ** 2), 1)

def get_category_and_tip(bmi):
    if bmi < 18.5:
        return "Underweight", "🌱 You're in the Underweight range. Time to nourish your body with a nutrient-rich diet and expert guidance. You’ve got this! 🍲"
    elif 18.5 <= bmi < 25:
        return "Normal", "🎯 You're in the Normal range—awesome job! Keep up the balanced diet and regular movement. Your consistency is your superpower 👍"
    else:
        return "Overweight", "🔥 You're in the Overweight range. No worries—this is your moment to rise! Embrace physical activity and smart eating habits. Every step counts 🏃‍♂"

# --- Calculate Button ---
if st.button("Calculate BMI"):
    if name and age and height > 0 and weight > 0:
        bmi = calculate_bmi(height, weight)
        category, tip = get_category_and_tip(bmi)

        st.markdown("---")
        st.markdown("### 🧾 Your Results")
        st.metric(label="Your BMI", value=f"{bmi}")
        st.success(f"**Category:** {category}")
        st.info(f"**Recommendation:** {tip}")

        # Save to history
        st.session_state.bmi_history.append([name, age, height, weight, bmi, category])
    else:
        st.warning("Please enter your name, age, height, and weight to calculate your BMI.")

# --- Footer ---
st.markdown("---")
st.caption("This tool is your launchpad—not a diagnosis. For personalized medical advice, always consult a healthcare professional.")