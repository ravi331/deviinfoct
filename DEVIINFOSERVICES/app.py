import streamlit as st
import pandas as pd
import os
from datetime import datetime
from auth import login_sidebar
from admin import post_announcement
from registration import register_student

st.set_page_config(page_title="Annual Day Portal", layout="wide")
login_sidebar()
ss = st.session_state

if ss.get("logged_in"):
    st.title("🎓 Welcome to St. Gregorios School Portal")
    st.success(f"Logged in as: {ss.mobile} ({ss.role})")

    # Mascot logo
    mascot_path = os.path.join("images", "mascot.png")
    if os.path.exists(mascot_path):
        st.image(mascot_path, width=200)

    # Countdown timer
    event_date = datetime(2025, 12, 20, 18, 0)  # ✅ Correct: Dec 20, 6 PM

    now = datetime.now()
    remaining = event_date - now
    days, seconds = remaining.days, remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    st.info(f"⏳ Time until Annual Day: {days} days, {hours} hours, {minutes} minutes")

    # Tabs
    tabs = st.tabs(["🏠 Home", "📢 Announcements", "📝 Registration", "🖼️ Gallery"])

    with tabs[0]:  # Home
        st.markdown("Welcome to the Annual Day portal. Use the tabs to navigate.")

    with tabs[1]:  # Announcements
        st.header("📢 Announcements")
        if os.path.exists("announcements.csv"):
            df = pd.read_csv("announcements.csv")
            for _, row in df.iterrows():
                st.info(row["message"])
        else:
            st.info("No announcements yet.")
        if ss.get("role") == "admin":
            st.divider()
            post_announcement()

    with tabs[2]:  # Registration
        register_student()
        if ss.get("role") == "admin":
            st.header("📋 Registered Students")
            if os.path.exists("registrations.csv"):
                df = pd.read_csv("registrations.csv")
                if not df.empty:
                    st.dataframe(df)
                    csv_data = df.to_csv(index=False).encode("utf-8")
                    st.download_button("Download CSV", data=csv_data, file_name="registrations.csv")
                else:
                    st.info("No registrations yet.")
            else:
                st.info("No registrations found.")

    with tabs[3]:  # Gallery
        st.header("🖼️ Event Gallery")
        st.info("Gallery feature coming soon!")
else:
    st.warning("🔒 Please log in to access the portal.")

