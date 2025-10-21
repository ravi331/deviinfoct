import streamlit as st
from utils import load_csv, safe_path
from datetime import datetime

def registration_form():
    st.header("Register for Annual Day Event")

    with st.form("register_form"):
        ss = st.session_state
        name = st.text_input("Student Name")
        clas = st.text_input("Class")
        sec = st.text_input("Section")
        item = st.text_input("Event/Item")
        addr = st.text_area("Address")
        bus = st.radio("Using Bus?", ["Yes", "No"])
        contact = st.text_input("Contact", value=ss.get("mobile", ""))

        if st.form_submit_button("Submit"):
            df = load_csv(
                safe_path("registrations.csv"),
                ["Timestamp", "Name", "Class", "Section", "Item", "Address", "Bus", "Contact", "Status"]
            )
            df.loc[len(df)] = [
                datetime.now(), name, clas, sec, item, addr, bus, contact, "Pending"
            ]
            df.to_csv(safe_path("registrations.csv"), index=False)
            st.success("✅ Registered Successfully!")

    st.subheader("Registered Students")
    data = load_csv(
        safe_path("registrations.csv"),
        ["Timestamp", "Name", "Class", "Section", "Item", "Address", "Bus", "Contact", "Status"]
    )
    st.dataframe(data, use_container_width=True)

    csv_data = data.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download CSV", csv_data, "registrations.csv", "text/csv")
