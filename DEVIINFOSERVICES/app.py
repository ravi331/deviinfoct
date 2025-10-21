import streamlit as st
import pandas as pd
import os
from datetime import datetime
from auth import login_sidebar
from admin import post_announcement
from registration import register_student

st.set_page_config(page_title="Annual Day Portal", layout="wide")
login_sidebar()
if st.session_state.get("logged_in"):
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

ss = st.session_state

if ss.get("logged_in"):
    st.title("🎓 Welcome to St. Gregorios School Portal")
    st.success(f"Logged in as: {ss.name} ({ss.role})")

    # Mascot logo
    mascot_path = os.path.join("images", "mascot.png")
    if os.path.exists(mascot_path):
        st.image(mascot_path, width=250)

    # Countdown to 20 Dec 2025, 6:00 PM
    event_date = datetime(2025, 12, 20, 18, 0)
    now = datetime.now()
    remaining = event_date - now
    days = remaining.days
    hours = remaining.seconds // 3600
    minutes = (remaining.seconds % 3600) // 60
    st.info(f"⏳ Time until Annual Day: {days} days, {hours} hours, {minutes} minutes")

    # Tabs
    tabs = st.tabs(["🏠 Home", "📢 Announcements", "📝 Registration", "🖼️ Gallery"])

    # Home tab
    with tabs[0]:
        st.markdown("Welcome to the Annual Day portal. Use the tabs to navigate.")

    # Announcements tab
    with tabs[1]:
        st.header("📢 Announcements")
        if os.path.exists("announcements.csv"):
            df = pd.read_csv("announcements.csv")
            for _, row in df[::-1].iterrows():
                st.info(f"📢 {row['message']}")

        else:
            st.info("No announcements yet.")

        if ss.get("role") == "admin":
            st.divider()
            post_announcement()
            manage_announcements()


    # Registration tab
    with tabs[2]:
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

    # Gallery tab
    with tabs[3]:
        st.header("🖼️ Event Gallery")

        if ss.get("role") == "admin":
            uploaded = st.file_uploader("Upload photo or video", type=["png", "jpg", "jpeg", "mp4", "mov"])

            if uploaded:
                os.makedirs("gallery", exist_ok=True)
                save_path = os.path.join("gallery", uploaded.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded.getbuffer())
                st.success("✅ Photo uploaded!")

        if os.path.exists("gallery"):
            images = [f for f in os.listdir("gallery") if f.lower().endswith((".png", ".jpg", ".jpeg"))]
            for img in images:
                st.image(os.path.join("gallery", img), use_column_width=True)
        else:
            st.info("No gallery images yet.")
else:
    st.warning("🔒 Please log in to access the portal.")




