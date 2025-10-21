import streamlit as st
import pandas as pd
import os
from auth import login_sidebar
from admin import post_announcement

st.set_page_config(page_title="School App", layout="centered")
login_sidebar()

ss = st.session_state

if ss.get("logged_in"):
    st.title("🎓 Welcome to St. Gregorios School Portal")

    # Show announcements
    st.header("📢 Announcements")
    if os.path.exists("announcements.csv"):
        df = pd.read_csv("announcements.csv")
        for _, row in df.iterrows():
            st.info(f"{row['message']}")
    else:
        st.info("No announcements yet.")

    # Admin-only section
    if ss.get("role") == "admin":
        st.divider()
        post_announcement()
else:
    st.warning("🔒 Please log in to view announcements.")
