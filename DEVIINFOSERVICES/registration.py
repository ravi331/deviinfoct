import streamlit as st
import pandas as pd
import os
from datetime import datetime

def register_student():
    ss = st.session_state

    st.subheader("📝 Student Registration")

    with st.form("registration_form"):
        name = st.text_input("Name")
        student_class = st.selectbox("Class", ["Nursery", "LKG", "UKG"] + [str(i) for i in range(1, 13)])
        section = st.text_input("Section")
        item = st.text_input("Item (e.g., Dance, Skit, Speech)")
        address = st.text_area("Address")
        bus = st.selectbox("Bus Required?", ["Yes", "No"])
        contact = st.text_input("Contact Number")
        status = st.selectbox("Status", ["Confirmed", "Pending"])

        submitted = st.form_submit_button("Submit")

    if submitted:
        if name.strip() and contact.strip():
            new_entry = {
                "timestamp": datetime.now().isoformat(),
                "name": name.strip(),
                "class": student_class,
                "section": section.strip(),
                "item": item.strip(),
                "address": address.strip(),
                "bus": bus,
                "contact": contact.strip(),
                "status": status
            }

            # Load existing data
            if os.path.exists("registrations.csv"):
                df = pd.read_csv("registrations.csv")
            else:
                df = pd.DataFrame(columns=new_entry.keys())

            # Add new entry at the top
            df = pd.concat([pd.DataFrame([new_entry]), df], ignore_index=True)
            df.to_csv("registrations.csv", index=False)
            st.success("✅ Registration submitted!")
            st.rerun()
        else:
            st.error("❌ Name and Contact are required.")
