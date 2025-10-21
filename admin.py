import streamlit as st
import pandas as pd
import os
from datetime import datetime

def post_announcement():
    ss = st.session_state

    if ss.get("role") != "admin":
        st.warning("🚫 Only admins can post announcements.")
        return

    st.subheader("📢 Post New Announcement")
    message = st.text_area("Enter your announcement")

    if st.button("Post"):
        if message.strip():
            # Load existing announcements
            if os.path.exists("announcements.csv"):
                df = pd.read_csv("announcements.csv")
            else:
                df = pd.DataFrame(columns=["timestamp", "message"])

            # Add new announcement at the top
            new_entry = {
                "timestamp": datetime.now().isoformat(),
                "message": message.strip()
            }
            df = pd.concat([pd.DataFrame([new_entry]), df], ignore_index=True)
            df.to_csv("announcements.csv", index=False)
            st.success("✅ Announcement posted!")
            st.rerun()
        else:
            st.error("❌ Message cannot be empty.")
