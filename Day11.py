import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF
from datetime import datetime

# --- Constants ---
MENU = {
    "Plain Parotta": 30,
    "Egg Parotta": 50,
    "Chicken Parotta": 80,
    "Veg Kothu Parotta": 70,
    "Chicken Kothu Parotta": 100,
    "Cheese Parotta": 90
}
TAX_RATE = 0.05
TABLES = [1, 2, 3, 4, 5]

# --- Session State Initialization ---
if "order" not in st.session_state:
    st.session_state.order = {item: 0 for item in MENU}
if "order_history" not in st.session_state:
    st.session_state.order_history = []
if "table_status" not in st.session_state:
    st.session_state.table_status = {t: "Available" for t in TABLES}

# --- Sidebar: Customer Info ---
st.sidebar.title("🧑 Customer Info")
customer_name = st.sidebar.text_input("Name")
table_number = st.sidebar.selectbox("Table Number", TABLES)
manual_status = st.sidebar.selectbox("Set Table Status", ["Available", "Occupied", "Vacating Soon"])
st.session_state.table_status[table_number] = manual_status

# --- Title ---
st.title("🥘 Parotta Paradise: Billing App")

# --- Menu Selection ---
st.header("🧾 Menu")
for item, price in MENU.items():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"{item} - ₹{price}")
    with col2:
        qty = st.number_input(f"Qty", min_value=0, step=1, key=item)
        st.session_state.order[item] = qty

# --- Billing Summary ---
st.markdown("---")
st.header("💰 Bill Summary")

bill_items = []
subtotal = 0

for item, qty in st.session_state.order.items():
    if qty > 0:
        price = MENU[item]
        discount_rate = 0.15 if qty >= 4 else 0.05 if qty >= 3 else 0.0
        discount = round(price * qty * discount_rate, 2)
        total = price * qty - discount
        bill_items.append({
            "Item": item,
            "Qty": qty,
            "Unit Price": price,
            "Discount": f"₹{discount}",
            "Total": total
        })
        subtotal += total

tax = round(subtotal * TAX_RATE, 2)
grand_total = round(subtotal + tax, 2)

df = pd.DataFrame(bill_items)
if not df.empty:
    st.dataframe(df, use_container_width=True)
    st.write(f"**Subtotal:** ₹{subtotal}")
    st.write(f"**Tax (5%):** ₹{tax}")
    st.write(f"**Total:** ₹{grand_total}")
else:
    st.info("No items selected.")

# --- Save Order ---
if st.button("💾 Save Order"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.order_history.append({
        "timestamp": timestamp,
        "customer": customer_name,
        "table": table_number,
        "items": bill_items,
        "total": grand_total
    })
    st.session_state.table_status[table_number] = "Occupied"
    st.success("Order saved!")

# --- Download Invoice ---
st.markdown("---")
st.header("📥 Download Invoice")

def generate_csv():
    csv = df.copy()
    csv.loc[len(csv.index)] = ["", "", "", "Subtotal", subtotal]
    csv.loc[len(csv.index)] = ["", "", "", "Tax (5%)", tax]
    csv.loc[len(csv.index)] = ["", "", "", "Total", grand_total]
    return csv.to_csv(index=False).encode("utf-8")

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    def safe(text): return text.replace("₹", "Rs.")

    pdf.cell(200, 10, txt="Parotta Paradise Invoice", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Customer: {customer_name}", ln=True)
    pdf.cell(200, 10, txt=f"Table: {table_number}", ln=True)
    pdf.cell(200, 10, txt=f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)

    for row in bill_items:
        line = f"{row['Item']} x{row['Qty']} = Rs.{row['Total']} (Discount: {safe(row['Discount'])})"
        pdf.cell(200, 10, txt=safe(line), ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Subtotal: Rs.{subtotal}", ln=True)
    pdf.cell(200, 10, txt=f"Tax (5%): Rs.{tax}", ln=True)
    pdf.cell(200, 10, txt=f"Total: Rs.{grand_total}", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()

if not df.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("⬇️ Download CSV", data=generate_csv(), file_name="invoice.csv", mime="text/csv")
    with col2:
        st.download_button("⬇️ Download PDF", data=generate_pdf(), file_name="invoice.pdf", mime="application/pdf")

# --- Order History Dashboard ---
st.markdown("---")
st.header("📊 Order History")

if st.session_state.order_history:
    history_df = pd.DataFrame([{
        "Time": o["timestamp"],
        "Customer": o["customer"],
        "Table": o["table"],
        "Total": o["total"]
    } for o in st.session_state.order_history])
    st.dataframe(history_df, use_container_width=True)
else:
    st.info("No orders yet.")

# --- Live Table Status ---
st.markdown("---")
st.header("🟢 Live Table Status")

status_colors = {
    "Available": "🟢",
    "Occupied": "🔴",
    "Vacating Soon": "🟡"
}

cols = st.columns(len(TABLES))
for i, table in enumerate(TABLES):
    with cols[i]:
        status = st.session_state.table_status[table]
        st.markdown(f"### Table {table}")
        st.markdown(f"{status_colors[status]} {status}")