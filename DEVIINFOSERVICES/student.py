import streamlit as st
from utils import load_csv, safe_path

def student_dashboard():
    ss = st.session_state
    st.header("🎓 Student Dashboard")

    st.info(f"Welcome, {ss.get('mobile')}! Here's your registration status:")

    df = load_csv(
        safe_path("registrations.csv"),
        ["Timestamp", "Name", "Class", "Section", "Item", "Address", "Bus", "Contact", "Status"]
    )

    student_data = df[df["Contact"].astype(str).str[-10:] == ss.get("mobile")]

    if student_data.empty:
        st.warning("You have not registered for any event yet.")
    else:
        st.dataframe(student_data, use_container_width=True)
        csv_data = student_data.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Your Registration", csv_data, "my_registration.csv", "text/csv")
