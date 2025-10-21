import streamlit as st
import pandas as pd
import os

def post_announcement():
    st.subheader("📢 Post a New Announcement")
    message = st.text_area("Announcement Message")

    if st.button("Post Announcement"):
        if message.strip():
            new_announcement = pd.DataFrame([{"message": message.strip()}])

            # Append to existing file or create new
            if os.path.exists("announcements.csv"):
                existing = pd.read_csv("announcements.csv")
                combined = pd.concat([existing, new_announcement], ignore_index=True)
            else:
                combined = new_announcement

            combined.to_csv("announcements.csv", index=False)
            st.success("✅ Announcement posted!")
        else:
            st.warning("Please enter a message before posting.")
